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

data "aws_secretsmanager_secret" "django" {
    name = var.django_secret_name
}

data "aws_secretsmanager_secret_version" "django" {
    secret_id = data.aws_secretsmanager_secret.django.id
}

data "external" "django" {
    program = ["echo", "${data.aws_secretsmanager_secret_version.django.secret_string}"]
}

data "aws_ssm_parameter" "ecr_image_url" {
    name = "ecr_image_url"
}

data "aws_ssm_parameter" "dbhost" {
    name = "postgres_dbhost"
}

data "aws_ssm_parameter" "dbname" {
    name = "postgres_dbname"
}

data "aws_ssm_parameter" "dbport" {
    name = "postgres_dbport"
}

data "aws_ssm_parameter" "dbpwd" {
    name = "postgres_dbpwd"
}

data "aws_ssm_parameter" "dbuser" {
    name = "postgres_dbuser"
}

data "aws_ssm_parameter" "secret_key" {
    name = "secret_key"
}