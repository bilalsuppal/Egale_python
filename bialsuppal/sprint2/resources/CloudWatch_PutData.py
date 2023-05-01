import boto3
class AwsCloudwatch:
    def __init__(self):
        
        self.client = boto3.client('cloudwatch')
        
    def cloudwatch_put_date(self, namespace, metricName, dimensions, value):
        """ cloud Watch Data Template """
        self.client.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                'MetricName': metricName,
                'Dimensions': dimensions,
                'Value': value,
            },
        ]
    )