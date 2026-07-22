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

output "nat_gateway_id" {
  value = module.nat_gateway.nat_gateway_id
}

output "nat_gateway_public_ip" {
  value = module.nat_gateway.elastic_ip
}

output "public_route_table_id" {

  value = module.route_tables.public_route_table_id

}

output "private_route_table_id" {

  value = module.route_tables.private_route_table_id

}

output "eks_cluster_security_group_id" {
  value = module.security_groups.eks_cluster_security_group_id
}

output "worker_node_security_group_id" {
  value = module.security_groups.worker_node_security_group_id
}

output "application_security_group_id" {
  value = module.security_groups.application_security_group_id
}

output "eks_cluster_role_arn" {
  value = module.iam.eks_cluster_role_arn
}

output "worker_node_role_arn" {
  value = module.iam.worker_node_role_arn
}