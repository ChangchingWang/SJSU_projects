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
Update pizza_order table.
Parameters:
{
    order_id: order001
    update_key: size
    update_value: Large
}
Return: Done (when successful)
'''
def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pizza_order')
    
    response = table.update_item(
        Key={'order_id': event["order_id"]},
        UpdateExpression="set order_detail." + event["update_key"] + "=:v",
        ExpressionAttributeValues={
            ':v': event['update_value']
        },
        ReturnValues="UPDATED_NEW"
    )

    print("update pizza_order." + event["update_key"] + " succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return 'Done'