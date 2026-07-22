#############################
# Public Route Table
#############################

resource "aws_route_table" "public" {

  vpc_id = var.vpc_id

  route {

    cidr_block = "0.0.0.0/0"

    gateway_id = var.internet_gateway_id

  }

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-${var.environment}-public-rt"
    }
  )

}


# Private Route Table

resource "aws_route_table" "private" {

  vpc_id = var.vpc_id

  route {

    cidr_block = "0.0.0.0/0"

    nat_gateway_id = var.nat_gateway_id

  }

  tags = merge(
    var.tags,
    {
      Name = "${var.project_name}-${var.environment}-private-rt"
    }
  )

}

# Public Associations

resource "aws_route_table_association" "public_1" {

  subnet_id = var.public_subnet_ids[0]

  route_table_id = aws_route_table.public.id

}

resource "aws_route_table_association" "public_2" {

  subnet_id = var.public_subnet_ids[1]

  route_table_id = aws_route_table.public.id

}


# Private Associations


resource "aws_route_table_association" "private_1" {

  subnet_id = var.private_subnet_ids[0]

  route_table_id = aws_route_table.private.id

}

resource "aws_route_table_association" "private_2" {

  subnet_id = var.private_subnet_ids[1]

  route_table_id = aws_route_table.private.id

}