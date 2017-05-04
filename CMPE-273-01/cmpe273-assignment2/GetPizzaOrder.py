import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

'''
Parameters:
{
    order_id : order001
}
Return:
{
    order_id : order001,
    aaa : AAA,
    bbb : BBB
}
'''

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pizza_order')
    
    try:
        response = table.get_item(
            Key={'order_id': event['order_id']}
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("pizza_order GetItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))
        #return json.dumps(item, indent=4, cls=DecimalEncoder)
        return item