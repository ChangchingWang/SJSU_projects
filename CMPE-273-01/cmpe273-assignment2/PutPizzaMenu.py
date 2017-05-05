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
    table = dynamodb.Table('pizza_menu')
    
    response = table.put_item(
        Item={
            "menu_id":event['menu_id'],
            "selection":event['selection'],
            "size":event['size'],
            "price":event['price'],
            "size_price":{
                event['size'][0]:event['price'][0],
                event['size'][1]:event['price'][1], 
                event['size'][2]:event['price'][2], 
                event['size'][3]:event['price'][3], 
                event['size'][4]:event['price'][4] 
            },
            "store_hours":event['store_hours']
        }
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return 'Done'