resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = 3
  min_capacity       = 1
  resource_id        = "service/${aws_ecs_cluster.cluster.name}/${aws_ecs_service.service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
  role_arn           = aws_iam_role.ecs-autoscale-role.arn
}

# resource "aws_appautoscaling_policy" "ecs_memory" {
#   name               = "ecs-memory-${var.environment}"
#   policy_type        = "TargetTrackingScaling"
#   resource_id        = aws_appautoscaling_target.ecs_target.resource_id
#   scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
#   service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

#   target_tracking_scaling_policy_configuration {
#     predefined_metric_specification {
#       predefined_metric_type = "ECSServiceAverageMemoryUtilization"
#     }

#     target_value = 60
#   }
#   depends_on = [aws_appautoscaling_target.ecs_target]
# }

# resource "aws_appautoscaling_policy" "ecs_cpu" {
#   name                  = "ecs-cpu-${var.environment}"
#   policy_type           = "TargetTrackingScaling"
#   resource_id           = aws_appautoscaling_target.ecs_target.resource_id
#   scalable_dimension    = aws_appautoscaling_target.ecs_target.scalable_dimension
#   service_namespace     = aws_appautoscaling_target.ecs_target.service_namespace

#   target_tracking_scaling_policy_configuration {
#     predefined_metric_specification {
#       predefined_metric_type = "ECSServiceAverageCPUUtilization"
#     }

#     target_value = 60
#   }
#   depends_on = [aws_appautoscaling_target.ecs_target]
# }

resource "aws_appautoscaling_policy" "ecs_target_tracking_predefined_metric_policy" {
  name               = "ecs-request-count-${var.environment}"
  policy_type        = "TargetTrackingScaling"
  resource_id        = "${aws_appautoscaling_target.ecs_target.resource_id}"
  scalable_dimension = "${aws_appautoscaling_target.ecs_target.scalable_dimension}"
  service_namespace  = "${aws_appautoscaling_target.ecs_target.service_namespace}"

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label = "${aws_alb.alb.arn_suffix}/${aws_alb_target_group.tg.arn_suffix}"
    }

    target_value       = 300
    scale_in_cooldown  = 100
    scale_out_cooldown = 300
  }
}