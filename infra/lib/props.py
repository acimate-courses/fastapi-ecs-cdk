# -*- coding: utf-8 -*-
from dataclasses import dataclass

from aws_cdk import StackProps
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecr as ecr

@dataclass
class VpcStackProps(StackProps):
    stack_tags: list[tuple[str, str]]    
    deploy_environment: str

@dataclass
class EcsBlueGreenStackProps(StackProps):
    stack_tags: list[tuple[str, str]]    
    deploy_environment: str
    cluster: ecs.ICluster
    repository: ecr.IRepository
    vpc: ec2.IVpc

@dataclass
class BaseStackProps(StackProps):
    stack_tags: list[tuple[str, str]]    
    deploy_environment: str
    vpc: ec2.IVpc
    