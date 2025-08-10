# -*- coding: utf-8 -*-
from aws_cdk import Environment, Stage
from constructs import Construct
from lib.props import VpcStackProps, EcsBlueGreenStackProps, BaseStackProps
from lib.stacks.vpc_stack import VpcStack
from lib.stacks.ecs_blue_green_stack import EcsBlueGreenStack
from lib.stacks.base_stack import BaseStack


class DevStage(Stage):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env: Environment,
        project_name: str,
        app_tags: list[tuple[str, str]],
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        deploy_environment = "dev"

        vpc_stack = VpcStack(
            self,
            f"{project_name}-{env.region}-vpc",
            props=VpcStackProps(
                deploy_environment=deploy_environment,
                stack_tags=app_tags,                
            ),
            env=Environment(account=env.account, region=env.region),
        )
        
        base_stack = BaseStack(
            self,
            f"{project_name}-{env.region}-base",
            props=BaseStackProps(
                deploy_environment=deploy_environment,
                stack_tags=app_tags,
                vpc=vpc_stack.vpc
            ),
            env=Environment(account=env.account, region=env.region),
        )
        
        # ecs_bg_stack = EcsBlueGreenStack(
        #     self,
        #     f"{project_name}-{env.region}-ecs-blue-green",
        #     props=EcsBlueGreenStackProps(
        #         deploy_environment=deploy_environment,
        #         stack_tags=app_tags,
        #         vpc=vpc_stack.vpc,
        #         cluster=base_stack.cluster,
        #         repository=base_stack.repository,
        #     ),
        #     env=Environment(account=env.account, region=env.region),
        # )
        