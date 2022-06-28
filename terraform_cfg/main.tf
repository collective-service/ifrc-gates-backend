terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.8.0"
    }
  }
  required_version = "1.1.2"
  backend "s3" {
    bucket          = "terraform-state-rcce"
    key             = "terraform.tfstate"
    region          = "eu-west-3"
#   dynamodb_table  = "terraform-lock-integration-db"
    encrypt         = true
    profile         = "dfs-rcce"
  }
}

provider "aws" {
  region                    = var.aws_region
  profile                   = var.aws_profile
  #shared_credentials_files = ["~/.aws/credentials"]
}