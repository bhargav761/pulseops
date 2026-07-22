resource "aws_subnet" "public_1" {

  vpc_id                  = var.vpc_id
  cidr_block              = var.public_subnet_1_cidr
  availability_zone       = var.availability_zone_1
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-public-1"

    "kubernetes.io/role/elb" = "1"
  })
}

resource "aws_subnet" "public_2" {

  vpc_id                  = var.vpc_id
  cidr_block              = var.public_subnet_2_cidr
  availability_zone       = var.availability_zone_2
  map_public_ip_on_launch = true

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-public-2"

    "kubernetes.io/role/elb" = "1"
  })
}

resource "aws_subnet" "private_1" {

  vpc_id            = var.vpc_id
  cidr_block        = var.private_subnet_1_cidr
  availability_zone = var.availability_zone_1

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-private-1"

    "kubernetes.io/role/internal-elb" = "1"
  })
}

resource "aws_subnet" "private_2" {

  vpc_id            = var.vpc_id
  cidr_block        = var.private_subnet_2_cidr
  availability_zone = var.availability_zone_2

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-private-2"

    "kubernetes.io/role/internal-elb" = "1"
  })
}