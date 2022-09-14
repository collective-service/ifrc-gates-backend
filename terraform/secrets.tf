data "aws_ssm_parameter" "ecr_backend_image_url" {
    name = "ecr_backend_image_url"
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