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


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pizza_order')
    
    response = table.put_item(
        Item={
            "order_id" : event['order_id'],
            "menu_id" : event['menu_id'],
            "customer_name" : event['customer_name'],
            "customer_email" : event['customer_email'],
            "order_status" : "processing",
            "order_detail" : {
                "selection" : "none",
                "size" : "none",
                "costs" : "none",
                "order_time" : "none"
            }
        }
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return 'Done'