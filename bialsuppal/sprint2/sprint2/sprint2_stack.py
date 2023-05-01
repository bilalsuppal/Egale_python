from aws_cdk import (
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as target_,
    Duration,
    RemovalPolicy,
    # Duration,
    Stack,
    aws_iam as iam,
    aws_cloudwatch as cw_,
    # aws_sqs as sqs,
)
from constructs import Construct
from resources import constants as constants
class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role=self.create_lambda_role()

        fn = self.create_lambda("WHLambda", "./resources", "WHapp.lambda_handler",lambda_role)
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
        schedule = events_.Schedule.rate(Duration.minutes(1))
        
        
        
        target = target_.LambdaFunction(handler=fn)
        
        rule = events_.Rule(self, "WHRule",

            schedule = schedule,
            targets = [target]
        
        )
        rule.apply_removal_policy(RemovalPolicy.DESTROY)
        
        dimensions={"Url":constants.site_url}
        availability_metric=cw_.Metric(
            metric_name = constants.AvailbilityMetrics,
            namespace = constants.namespace,
            dimensions_map= dimensions
        )
        availability_alarm=cw_.Alarm(self, "availabilityErrors",
            metric=availability_metric,
            evaluation_periods=1,
            threshold=1,
            comparison_operator=cw_.ComparisonOperator.LESS_THAN_THRESHOLD
            
        ) 

        latency_metric=cw_.Metric(
            metric_name = constants.latencyMetrics,
            namespace = constants.namespace,
            dimensions_map= dimensions
        )
        latency_alarm=cw_.Alarm(self, "latencyErrors",
            metric=latency_metric,
            evaluation_periods=1,
            threshold=0.5,
            comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD
            
        )
    def create_lambda(self, id, asset, handler,lambda_role):
        return lambda_.Function(self, 
            id = id,
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler=handler,
            code=lambda_.Code.from_asset(asset),
            role=lambda_role
        )


    def create_lambda_role(self):
        return iam.Role(self, "Bilal_lambda_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")]
        ) 


        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint2Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
