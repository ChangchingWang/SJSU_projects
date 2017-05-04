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
    
    try:
        response = table.get_item(
            Key={'menu_id': event['menu_id']}
        )
    except Exception as e:
        print(e)
    else:
        item = response['Item']
        print("GetItem succeeded:")
        print(json.dumps(item["selection"], indent=4, cls=DecimalEncoder))
        selections = {}
        for idx, val in enumerate(item["selection"]):
            selections[str(idx+1)] = val
        #return json.dumps(selections, indent=4, cls=DecimalEncoder)
        return selections