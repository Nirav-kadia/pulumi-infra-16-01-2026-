import pulumi_aws as aws
import json

ecs_execution_role = aws.iam.Role(
    "ecs-execution-role",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
            "Action": "sts:AssumeRole",
        }]
    }),
)

aws.iam.RolePolicyAttachment(
    "ecs-task-exec-policy",
    role=ecs_execution_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
)
