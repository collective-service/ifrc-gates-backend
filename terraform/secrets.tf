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

data "aws_ssm_parameter" "s3_bucket_name" {
    name = "s3_backend_bucket_name"
}

data "aws_ssm_parameter" "http_protocol" {
    name = "http_protocol"
}

data "aws_ssm_parameter" "cors_allowed_origins" {
    name = "cors_allowed_origins"
}

resource "aws_ssm_parameter" "celery_redis_url" {
    name    = "celery_redis_url"
    type    = "SecureString"
    value   = "redis://${aws_elasticache_cluster.redis.cache_nodes[0].address}:${aws_elasticache_cluster.redis.cache_nodes[0].port}/0"
}

resource "aws_ssm_parameter" "django_cache_redis_url" {
    name    = "django_cache_redis_url"
    type    = "SecureString"
    value   = "redis://${aws_elasticache_cluster.redis.cache_nodes[0].address}:${aws_elasticache_cluster.redis.cache_nodes[0].port}/1"
}