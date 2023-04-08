from aws_cdk import (
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as target_,
    Duration,
    RemovalPolicy,
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        fn = self.create_lambda("WHLambda", "./resources", "WHapp.lambda_handler")
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
        schedule = events_.Schedule.rate(Duration.minutes(60))
        
        
        
        target = target_.LambdaFunction(handler=fn)
        
        rule = events_.Rule(self, "WHRule",

            schedule = schedule,
            targets = [target]
        
        )        
            
            
    def create_lambda(self, id, asset, handler):
        return lambda_.Function(self, 
            id = id,
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler=handler,
            code=lambda_.Code.from_asset(asset)
        )


        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint2Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
