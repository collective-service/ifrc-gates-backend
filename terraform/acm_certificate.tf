provider "aws" {
  alias = "virginia"
  region = "us-east-1"
  profile = var.aws_profile
}

# resource "aws_acm_certificate" "acm_certificate1" {
#   domain_name               = "backend.rjstharcce.cloudns.ph"
#   subject_alternative_names = ["*.backend.rjstharcce.cloudns.ph"]
#   validation_method         = "DNS"

#   lifecycle {
#     create_before_destroy = true
#   }
# }

# request public certificates from the amazon certificate manager.
resource "aws_acm_certificate" "acm_certificate" {
  #provider                  = aws.virginia
  domain_name               = "backend.rjstharcce.cloudns.ph"
  subject_alternative_names = ["*.backend.rjstharcce.cloudns.ph"]
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# get details about a route 53 hosted zone
data "aws_route53_zone" "route53_zone" {
  name         = "backend.rjstharcce.cloudns.ph"
  private_zone = false
}

# create a record set in route 53 for domain validatation
resource "aws_route53_record" "route53_record" {
  for_each = {
    for dvo in aws_acm_certificate.acm_certificate.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.route53_zone.zone_id
}

# validate acm certificates
resource "aws_acm_certificate_validation" "acm_certificate_validation" {
  #provider                = aws.virginia
  certificate_arn         = aws_acm_certificate.acm_certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.route53_record : record.fqdn]
}