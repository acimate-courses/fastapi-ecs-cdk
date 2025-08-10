from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_s3 as s3,
)
from constructs import Construct
from lib.props import VpcStackProps

class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, props: VpcStackProps, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket to store VPC Flow Logs
        flow_log_bucket = s3.Bucket(
            self, 
            "TrainingVpcFlowLogBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Create a VPC spanning 2 AZs, with public and private subnets and a single NAT Gateway
        self.vpc = ec2.Vpc(
            self, "AppVpc",
            cidr="10.0.0.0/16",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask=24
                )
            ]
        )

        # Export the subnets and VPC ID for reference
        self.public_subnets = self.vpc.select_subnets(
            subnet_type=ec2.SubnetType.PUBLIC
        ).subnet_ids

        self.private_subnets = self.vpc.select_subnets(
            subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
        ).subnet_ids

        # Enable VPC Flow Logs, deliver to S3 bucket
        ec2.FlowLog(
            self, "TrainingVpcFlowLogs",
            resource_type=ec2.FlowLogResourceType.from_vpc(self.vpc),
            destination=ec2.FlowLogDestination.to_s3(flow_log_bucket)
        )
        