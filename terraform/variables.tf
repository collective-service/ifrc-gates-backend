variable aws_region {}

variable aws_profile {}

variable az_count {}

variable environment {}

variable app_port {}

variable "ecs_task_execution_role" {}

variable health_check_path {}

variable fargate_cpu {}

variable fargate_memory {}

variable app_count {}

# Redis
variable redis_cluster_name {}
variable redis_node_type {}
variable redis_num_cache_nodes {}
variable redis_port {}

# Secrets
variable backend_ecr_secret_name {}

# Postgres
variable postgres_secret_name {}

# Django
variable django_secret_name {}