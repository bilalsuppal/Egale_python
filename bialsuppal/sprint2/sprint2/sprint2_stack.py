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
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_cloudwatch_actions as cw_actions,
    # aws_sqs as sqs,
    aws_dynamodb as db_,
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
        dbLambda=self.create_lambda("DBLambda", "./resources", "DBapp.lambda_handler",lambda_role)
        
        
        target = target_.LambdaFunction(handler=fn)
        
        rule = events_.Rule(self, "WHRule",

            schedule = schedule,
            targets = [target]
        
        )
        rule.apply_removal_policy(RemovalPolicy.DESTROY)
        
        topic = sns.Topic(self, "WHNotification")
        topic.add_subscription(subscriptions.EmailSubscription("bilal.hussain2332@gmail.com"))

        for i in range(len(constants.site_url)):
            dimensions={"Url":constants.site_url[i]}
            availability_metric=cw_.Metric(
                metric_name = constants.AvailbilityMetrics,
                namespace = constants.namespace,
                dimensions_map= dimensions
            )
            availability_alarm=cw_.Alarm(self, f"availabilityErrors_{i}",
                metric=availability_metric,
                evaluation_periods=1,
                threshold=1,
                comparison_operator=cw_.ComparisonOperator.LESS_THAN_THRESHOLD
                
            ) 
            availability_alarm.add_alarm_action(cw_actions.SnsAction(topic))

            latency_metric=cw_.Metric(
                metric_name = constants.latencyMetrics,
                namespace = constants.namespace,
                dimensions_map= dimensions
            )
            latency_alarm=cw_.Alarm(self, f"latencyErrors_{i}",
                metric=latency_metric,
                evaluation_periods=1,
                threshold=0.5,
                comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD
                
            )
            latency_alarm.add_alarm_action(cw_actions.SnsAction(topic))
            
            dbTable=self.create_dynamoDB_table()
            dbTable.grant_read_write_data(dbLambda)
            db_lambda_function.add_enviroment("table_name",db_table.table_name)

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

    def create_dynamodb_table(self):
        table = db_.Table(self, "AlarmTable",
            partition_key=db_.Attribute(name="id", type=db_.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY,
            sort_key= .....<timestamp>
        return table
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint2Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
