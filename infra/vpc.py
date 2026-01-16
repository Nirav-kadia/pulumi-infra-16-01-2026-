import pulumi_aws as aws

# -----------------
# VPC
# -----------------
vpc = aws.ec2.Vpc(
    "django-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
)

# -----------------
# Subnets
# -----------------
public_subnet = aws.ec2.Subnet(
    "public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
)

private_subnet = aws.ec2.Subnet(
    "private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
)

# ✅ THIS LINE MUST EXIST
private_subnets = [private_subnet.id]

# -----------------
# Internet Gateway
# -----------------
internet_gateway = aws.ec2.InternetGateway(
    "igw",
    vpc_id=vpc.id,
)

# -----------------
# ECS Security Group
# -----------------
ecs_security_group = aws.ec2.SecurityGroup(
    "ecs-sg",
    vpc_id=vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=8000,
            to_port=8000,
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
        )
    ],
)
