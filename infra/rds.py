import pulumi_aws as aws

db = aws.rds.Instance(
    "django-db",
    engine="postgres",
    engine_version="13.20",
    instance_class="db.t3.micro",
    allocated_storage=20,

    db_name="djangodb",
    username="django",
    password="supersecret",

    skip_final_snapshot=True,
    publicly_accessible=False,
)
