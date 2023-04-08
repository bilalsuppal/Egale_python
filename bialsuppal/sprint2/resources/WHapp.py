import urllib3
import datetime

url="hicotex.com"

def lambda_handler(event,context):
    values=dict()
    availability=getAvail();
    latency=getLatency();
    values.update({"availability":availability,"latency":latency})
    return values

def getAvail():
    http=urllib3.PoolManager()
    response = http.request("Get",url)
    if response.status==200:
        return 1.0
    else:
        return 0.0
    
def getLatency():
    http=urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request("Get", url)
    response = http.request("Get", url)
    end =datetime.datetime.now()
    delta = end -start
    latencySec = round(delta.microseconds*.00001,6)
    return latencySec