import pulumi_aws as aws

task = aws.ecs.TaskDefinition(
    "django-task",
    family="django",
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=ecs_role.arn,
    container_definitions=pulumi.Output.all(
        repo.repository_url, db.address
    ).apply(lambda args: f"""
    [{
        "name": "django",
        "image": "{args[0]}:latest",
        "portMappings": [{"containerPort": 8000}],
        "environment": [
            {{"name": "DB_HOST", "value": "{args[1]}"}}
        ]
    }]
    """),
)
