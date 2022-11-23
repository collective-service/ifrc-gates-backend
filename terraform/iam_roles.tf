data "aws_iam_policy_document" "ecs_task_execution_role" {
  version = "2012-10-17"
  statement {
    sid     = ""
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "${var.ecs_task_execution_role}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "param_store" {
  name = "secrets-paramstore"
  role = aws_iam_role.ecs_task_execution_role.id
  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "ssm:GetParameters"
        ],
        "Effect": "Allow",
        "Resource": [
          "${data.aws_ssm_parameter.dbname.arn}",
          "${data.aws_ssm_parameter.dbuser.arn}",
          "${data.aws_ssm_parameter.dbpwd.arn}",
          "${data.aws_ssm_parameter.dbhost.arn}",
          "${data.aws_ssm_parameter.dbport.arn}",
          "${data.aws_ssm_parameter.secret_key.arn}",
          "${data.aws_ssm_parameter.s3_bucket_name.arn}",
          "${aws_ssm_parameter.celery_redis_url.arn}",
          "${aws_ssm_parameter.django_cache_redis_url.arn}",
          "${data.aws_ssm_parameter.http_protocol.arn}",
          "${data.aws_ssm_parameter.cors_allowed_origins.arn}",
          "${data.aws_ssm_parameter.app_type.arn}",
          "${data.aws_ssm_parameter.rcce_cs_environment.arn}",
          "${data.aws_ssm_parameter.sentry_dsn.arn}",
          "${data.aws_ssm_parameter.react_app_api_end.arn}",
          "${data.aws_ssm_parameter.react_app_api_https.arn}"
        ]
      }
    ]
  }
  EOF
}

resource "aws_iam_role" "ecs_task" {
    name = "${var.ecs_task_role}-${var.environment}"
    assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json
}

resource "aws_iam_role_policy" "ecs-role-policy" {
    name = "ecs-role-policy-${var.environment}"
    role = aws_iam_role.ecs_task.id
    policy = <<-EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ssmmessages:CreateControlChannel",
                    "ssmmessages:CreateDataChannel",
                    "ssmmessages:OpenControlChannel",
                    "ssmmessages:OpenDataChannel",
                    "s3:*",
                    "rds:*",
                    "elasticache:*",
                    "rds-db:connect"
                ],
                "Resource": "*"
            }
        ]
    }
    EOF
}

resource "aws_iam_role" "ecs-autoscale-role" {
  name = "ecs-scale-application-${var.environment}"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "application-autoscaling.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs-autoscale" {
  role = aws_iam_role.ecs-autoscale-role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceAutoscaleRole"
}