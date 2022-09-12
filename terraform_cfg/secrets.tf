data "aws_secretsmanager_secret" "ecr_backend_url" {
    name = var.backend_ecr_secret_name
}

data "aws_secretsmanager_secret_version" "ecr_backend_url" {
    secret_id = data.aws_secretsmanager_secret.ecr_backend_url.id
}

data "external" "ecr_backend" {
    program = ["echo", "${data.aws_secretsmanager_secret_version.ecr_backend_url.secret_string}"]
}

data "aws_secretsmanager_secret" "postgres" {
    name = var.postgres_secret_name
}

data "aws_secretsmanager_secret_version" "postgres" {
    secret_id = data.aws_secretsmanager_secret.postgres.id
}

data "external" "postgres_creds" {
    program = ["echo", "${data.aws_secretsmanager_secret_version.postgres.secret_string}"]
}