from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
)
from constructs import Construct
from lib.props import BaseStackProps

class BaseStack(Stack):
    def __init__(self, scope: Construct, id: str, props: BaseStackProps, **kwargs):
        super().__init__(scope, id, **kwargs)
        

        # 1) ECS Cluster
        cluster = ecs.Cluster(self, "FastapiEcsTrainingCluster", vpc=props.vpc)

        # 3) ECR Repository for your Python FastAPI Docker image
        repository = ecr.Repository(
            self, "AppRepo",
            repository_name="fastapi-app",
            removal_policy=RemovalPolicy.RETAIN
        )

        # Export for other stacks        
        self.cluster    = cluster
        self.repository = repository
        