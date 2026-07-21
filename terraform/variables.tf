variable "project_name" {

  description = "Project Name"

  type = string

  default = "pulseops"

}

variable "environment" {

  description = "Deployment Environment"

  type = string

  default = "dev"

}

variable "owner" {

  description = "Infrastructure Owner"

  type = string

  default = "Bhargava"

}

variable "aws_region" {

  description = "AWS Region"

  type = string

  default = "ap-south-1"

}