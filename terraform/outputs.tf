#################################################
# Root Outputs
#################################################

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "vpc_arn" {
  value = module.vpc.vpc_arn
}

output "vpc_cidr" {
  value = module.vpc.vpc_cidr
}

output "default_route_table_id" {
  value = module.vpc.default_route_table_id
}

output "default_network_acl_id" {
  value = module.vpc.default_network_acl_id
}

output "default_security_group_id" {
  value = module.vpc.default_security_group_id
}

output "public_subnet_ids" {
  value = module.subnets.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.subnets.private_subnet_ids
}

output "internet_gateway_id" {
  value = module.internet_gateway.igw_id
}