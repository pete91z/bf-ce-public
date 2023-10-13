# Lambda triggered by write to Kinesis stream. Payload is read, and forwarded to an appropriate firehose
# stream based on the item type
import base64
import json
import boto3

client = boto3.client('firehose')

print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        pl = json.loads(payload)
        if pl['item'] == 'ORDER':
            response = client.put_record(
                DeliveryStreamName='orders-put',
                Record = { 
                    'Data': (json.dumps(pl)+"\n").encode('utf-8')
                }
            )
        elif pl['item'] == 'STOCK':
            response = client.put_record(
                 DeliveryStreamName='stock-put',
                 Record = { 
                     'Data': (json.dumps(pl)+"\n").encode('utf-8')
                 }
            )            
        print("Decoded payload: " + payload)
        
    return 'Successfully processed {} records.'.format(len(event['Records']))
