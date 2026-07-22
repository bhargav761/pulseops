output "eks_cluster_security_group_id" {
  value = aws_security_group.eks_cluster.id
}

output "worker_node_security_group_id" {
  value = aws_security_group.worker_nodes.id
}

output "application_security_group_id" {
  value = aws_security_group.application.id
}