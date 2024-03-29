resource "aws_ecs_cluster" "cluster" {
  name = "cluster-rcce-backend-${var.environment}"
}

data "template_file" "config" {
  template = file("./templates/ecr_image/image.json")

  vars = {
    app_image      = "${data.aws_ssm_parameter.ecr_backend_image_url.value}:latest"
    app_port       = var.app_port
    fargate_cpu    = var.fargate_cpu
    fargate_memory = var.fargate_memory
    aws_region     = var.aws_region
    environment    = var.environment
    # Redis
    celery_redis_url = aws_ssm_parameter.celery_redis_url.arn
    django_cache_redis_url = aws_ssm_parameter.django_cache_redis_url.arn
    # Postgresql credentials
    db_name = data.aws_ssm_parameter.dbname.arn
    db_user = data.aws_ssm_parameter.dbuser.arn
    db_pwd  = data.aws_ssm_parameter.dbpwd.arn
    db_host = data.aws_ssm_parameter.dbhost.arn
    db_port = data.aws_ssm_parameter.dbport.arn
    # Django
    secret_key = data.aws_ssm_parameter.secret_key.arn
    debug = "False"
    use_local_storage = "False"
    s3_bucket_name = data.aws_ssm_parameter.s3_bucket_name.arn
    http_protocol = data.aws_ssm_parameter.http_protocol.arn
    cors_allowed_origins = data.aws_ssm_parameter.cors_allowed_origins.arn
    app_type = data.aws_ssm_parameter.app_type.arn
    rcce_cs_environment = data.aws_ssm_parameter.rcce_cs_environment.arn
    sentry_dsn = data.aws_ssm_parameter.sentry_dsn.arn
  }
}

resource "aws_ecs_task_definition" "task-def" {
  family                   = "backend-app-task-${var.environment}"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  container_definitions    = data.template_file.config.rendered

  depends_on = [
    aws_ssm_parameter.celery_redis_url,
    aws_ssm_parameter.django_cache_redis_url
  ]
}

resource "aws_ecs_service" "service" {
  name            = "backend-service-${var.environment}"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task-def.arn
  desired_count   = var.app_count
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = [
        aws_security_group.ecs_sg.id
    ]
    subnets          = aws_subnet.private.*.id
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.tg.arn
    container_name   = "backend-app-${var.environment}"
    container_port   = var.app_port
  }

  depends_on = [
    aws_alb_listener.app_listener,
    aws_iam_role_policy_attachment.ecs_task_execution_role
  ]
}