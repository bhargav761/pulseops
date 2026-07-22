#################################################
# PulseOps Infrastructure
#################################################

module "vpc" {

  source = "./modules/vpc"

  project_name = var.project_name

  environment = var.environment

  vpc_cidr = "10.0.0.0/16"

  tags = local.common_tags

}
module "subnets" {

  source = "./modules/subnets"

  project_name = var.project_name
  environment  = var.environment

  vpc_id = module.vpc.vpc_id

  public_subnet_1_cidr = "10.0.1.0/24"
  public_subnet_2_cidr = "10.0.2.0/24"

  private_subnet_1_cidr = "10.0.11.0/24"
  private_subnet_2_cidr = "10.0.12.0/24"

  availability_zone_1 = "ap-south-1a"
  availability_zone_2 = "ap-south-1b"

  tags = local.common_tags

}

module "internet_gateway" {

  source = "./modules/internet-gateway"

  project_name = var.project_name
  environment  = var.environment

  vpc_id = module.vpc.vpc_id

  tags = local.common_tags

}

module "nat_gateway" {

  source = "./modules/nat-gateway"

  project_name = var.project_name
  environment  = var.environment

  public_subnet_id = module.subnets.public_subnet_ids[0]

  tags = local.common_tags

}

module "route_tables" {

  source = "./modules/route-tables"

  project_name = var.project_name
  environment  = var.environment

  vpc_id = module.vpc.vpc_id

  internet_gateway_id = module.internet_gateway.igw_id

  nat_gateway_id = module.nat_gateway.nat_gateway_id

  public_subnet_ids = module.subnets.public_subnet_ids

  private_subnet_ids = module.subnets.private_subnet_ids

  tags = local.common_tags

}

module "security_groups" {

  source = "./modules/security-groups"

  project_name = var.project_name
  environment  = var.environment

  vpc_id = module.vpc.vpc_id

  tags = local.common_tags
}