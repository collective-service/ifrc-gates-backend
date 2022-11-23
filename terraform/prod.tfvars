aws_region  = "eu-west-3"
aws_profile = "dfs-rcce"
environment = "prod"

# vpc
az_count = 2
cidr_block = "172.16.0.0/16"

# app
app_port = "7020"

# ECS role
ecs_task_execution_role = "ECSTaskExecutionRole"
ecs_task_role = "ECSTaskRole"

# alb
health_check_path = "/admin/"

# ECS
fargate_cpu = "1024"
fargate_memory = "2048"
app_count = 2

# Redis
redis_cluster_name = "redis"
redis_node_type = "cache.t2.micro"
redis_num_cache_nodes = 1
redis_port = 6379

# Secrets
backend_ecr_secret_name = "ecr/backend"

# Postgres
postgres_secret_name = "prod/postgres"

# Django
django_secret_name = "prod/django"

# Autoscaling
max_capacity = 3
min_capacity = 1
request_target_value = 300
scale_in_cooldown_secs = 100
scale_out_cooldown_secs = 300

# Route 53
domain_name = "ifrc-gates.dev.datafriendlyspace.org"