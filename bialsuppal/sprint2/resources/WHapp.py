# lambda function to check the health of the web server

values = dict()

import urllib3
import datetime
from CloudWatch_PutData import AwsCloudwatch
import constants as constant

def lambda_handler(event, context):
    
    cw_client = AwsCloudwatch()
    
    for i in range(len(constant.site_url)):
        avail = availbility(constant.site_url[i])
        late = latency(constant.site_url[i])
        
        
    
        dimensions = [{'Name': 'Url','Value': constant.site_url[i]}]
        
        cw_client.cloudwatch_put_date(constant.namespace, constant.AvailbilityMetrics, dimensions, avail)
        cw_client.cloudwatch_put_date(constant.namespace, constant.latencyMetrics, dimensions, late)
    
    
    # print(avail,late)
        values.update({f'{constant.site_url[i]}' : f'Availbility == > {avail} || Latency == > {late}'})
        
    return values

def availbility(Url):

    http = urllib3.PoolManager()

    response = http.request("GET", Url)

    if response.status == 200:
        return 1
    else:
        return 0
    
def latency(Url):
    
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request('GET', Url)
    end = datetime.datetime.now()
    
    delta = end - start
    
    latencySec = round(delta.microseconds * .000001, 6)
    
    return latencySec