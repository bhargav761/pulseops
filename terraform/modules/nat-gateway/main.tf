resource "aws_eip" "nat" {

  domain = "vpc"

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-${var.environment}-nat-eip"
    }
  )

}

resource "aws_nat_gateway" "this" {

  allocation_id = aws_eip.nat.id

  subnet_id = var.public_subnet_id

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-${var.environment}-nat"
    }
  )

  depends_on = [
    aws_eip.nat
  ]

}