aws_region  = "eu-west-3"
aws_profile = "dfs-rcce"
environment = "staging"

# vpc
az_count = 2

# app
app_port = "80"

# ECS role
ecs_task_execution_role = "ECSTaskExecutionRole"

# alb
health_check_path = "/"

# ECS
fargate_cpu = "1024"
fargate_memory = "2048"
app_count = 2
app_image = "nginx:latest"