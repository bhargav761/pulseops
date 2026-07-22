##############################
# EKS Control Plane Security Group
##############################

resource "aws_security_group" "eks_cluster" {

  name        = "${var.project_name}-${var.environment}-eks-cluster"
  description = "EKS Control Plane Security Group"
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-eks-cluster-sg"
  })
}

##############################
# Worker Node Security Group
##############################

resource "aws_security_group" "worker_nodes" {

  name        = "${var.project_name}-${var.environment}-worker"
  description = "Worker Node Security Group"
  vpc_id      = var.vpc_id

  ingress {
    from_port = 0
    to_port   = 65535
    protocol  = "tcp"
    self      = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-worker-sg"
  })
}

##############################
# Application Security Group
##############################

resource "aws_security_group" "application" {

  name        = "${var.project_name}-${var.environment}-app"
  description = "Application Security Group"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-app-sg"
  })
}