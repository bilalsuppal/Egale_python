from aws_cdk import (
    
    aws_lambda as lambda_,
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class Sprint1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fn = self.create_lambda("helloLambda", "./resources", "HelloWorldLambda.lambda_handler" )
            
            
            
    def create_lambda(self, id, asset, handler):
        return lambda_.Function(self, 
            id = id,
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler=handler,
            code=lambda_.Code.from_asset(asset)
        )
