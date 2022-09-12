resource "aws_ecs_cluster" "cluster" {
  name = "cluster-rcce-backend-${var.environment}"
}

data "template_file" "config" {
  template = file("./templates/ecr_image/image.json")

  vars = {
    app_image      = data.external.ecr_backend.result.ecr_backend_url # var.app_image
    app_port       = var.app_port
    fargate_cpu    = var.fargate_cpu
    fargate_memory = var.fargate_memory
    aws_region     = var.aws_region
    environment    = var.environment
    # Redis
    celery_redis_url = "redis://${aws_elasticache_cluster.redis.cache_nodes[0].address}:${aws_elasticache_cluster.redis.cache_nodes[0].port}/0"
    django_cache_redis_url = "redis://${aws_elasticache_cluster.redis.cache_nodes[0].address}:${aws_elasticache_cluster.redis.cache_nodes[0].port}/1"
    # Postgresql credentials
    db_name = data.external.postgres_creds.result.db_name
    db_user = data.external.postgres_creds.result.db_user
    db_pwd  = data.external.postgres_creds.result.db_pwd
    db_host = data.external.postgres_creds.result.db_host
    db_port = data.external.postgres_creds.result.db_port
    # Django
    secret_key = data.external.django.result.secret_key
    debug = data.external.django.result.debug
  }
}

resource "aws_ecs_task_definition" "task-def" {
  family                   = "backend-app-task-${var.environment}"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  container_definitions    = data.template_file.config.rendered
}

resource "aws_ecs_service" "service" {
  name            = "backend-service-${var.environment}"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task-def.arn
  desired_count   = var.app_count
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs_sg.id]
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