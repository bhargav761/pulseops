resource "aws_eks_cluster" "this" {

  name     = var.cluster_name
  role_arn = var.cluster_role_arn
  version  = var.cluster_version

  vpc_config {

    subnet_ids = var.subnet_ids

    security_group_ids = var.security_group_ids

    endpoint_private_access = true
    endpoint_public_access  = true

  }

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator"
  ]

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-${var.environment}-eks"
    }
  )

}