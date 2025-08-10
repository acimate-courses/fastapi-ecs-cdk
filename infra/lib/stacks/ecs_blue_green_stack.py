from aws_cdk import (
    Stack,
    Duration,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_ecs_patterns as ecs_patterns,
    aws_codedeploy as codedeploy,        
    aws_elasticloadbalancingv2 as elbv2
)
from constructs import Construct
from lib.props import EcsBlueGreenStackProps

class EcsBlueGreenStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        props: EcsBlueGreenStackProps,
        #cluster: ecs.ICluster,
        #repository: ecr.IRepository,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
            cluster=props.cluster,
            memory_limit_mib=512,
            desired_count=1,
            cpu=256,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(
                    repository=props.repository,
                    #tag=App.of(self).node.try_get_context("image_tag") or "latest"
                    tag = "latest"
            ),      
            ),
            min_healthy_percent=100,            
        )

        scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=2
        )

        scalable_target.scale_on_cpu_utilization("CpuScaling",
            target_utilization_percent=50
        )

        scalable_target.scale_on_memory_utilization("MemoryScaling",
            target_utilization_percent=50
        )                        