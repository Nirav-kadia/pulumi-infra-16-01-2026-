import pulumi_aws as aws

django_repo = aws.ecr.Repository(
    "django-ecr-repo",
    image_scanning_configuration={"scanOnPush": True},
)

