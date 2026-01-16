import pulumi
import pulumi_aws as aws
from ecr import django_repo
from iam import ecs_execution_role
from rds import db
from vpc import private_subnets, ecs_security_group

cluster = aws.ecs.Cluster("django-cluster")

task_definition = aws.ecs.TaskDefinition(
    "django-task",
    family="django-task",
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=ecs_execution_role.arn,
    container_definitions=pulumi.Output.all(
        django_repo.repository_url,
        db.address,
    ).apply(lambda args: f"""
    [{
        "name": "django",
        "image": "{args[0]}:latest",
        "portMappings": [{
            "containerPort": 8000,
            "protocol": "tcp"
        }],
        "essential": true,
        "environment": [
            {{"name": "DB_HOST", "value": "{args[1]}"}},
            {{"name": "DB_NAME", "value": "djangodb"}},
            {{"name": "DB_USER", "value": "django"}},
            {{"name": "DB_PASSWORD", "value": "supersecret"}}
        ]
    }]
    """),
)


service = aws.ecs.Service(
    "django-service",
    cluster=cluster.arn,
    task_definition=task_definition.arn,
    desired_count=1,
    launch_type="FARGATE",
    network_configuration={
        "subnets": private_subnets,
        "security_groups": [ecs_security_group.id],
        "assign_public_ip": False,
    },
)
