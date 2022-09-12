resource "aws_cloudwatch_log_group" "testapp_log_group" {
  name              = "/ecs/backend-${var.environment}"
  retention_in_days = 30

  tags = {
    Name = "cw-log-group-backend-${var.environment}"
  }
}

resource "aws_cloudwatch_log_stream" "myapp_log_stream" {
  name           = "log-stream-backend-${var.environment}"
  log_group_name = aws_cloudwatch_log_group.testapp_log_group.name
}