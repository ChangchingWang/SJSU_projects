import boto3
import json
import decimal
import collections
from datetime import datetime
from time import strftime

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def query_item(table_name, key_name, key_value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name) 
    try:
        response = table.get_item(
            Key={key_name: key_value}
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print(table_name + " GetItem succeeded:")
        #print(json.dumps(item, indent=4, cls=DecimalEncoder))
        return item

def update_order(order_id, size, costs, order_time):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pizza_order')

    response = table.update_item(
        Key={'order_id': order_id},
        UpdateExpression="set order_detail.size = :s, order_detail.costs = :c, order_detail.order_time = :o",
        ExpressionAttributeValues={
            ':s': size,
            ':c': costs,
            ':o': order_time
        },
        ReturnValues="UPDATED_NEW"
    )

    print("update pizza_order succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return 'Done'

def lambda_handler(event, context):
    
    # query menu_id of this order
    order = query_item('pizza_order', 'order_id', event["order_id"])
    
    # query size name of size number
    menu = query_item('pizza_menu', 'menu_id', order["menu_id"])
    sizeDic = {}
    for idx, val in enumerate(menu["size"]):
        sizeDic[str(idx+1)] = val
    
    size = sizeDic[event["input"]] # 1. Slide, 2. Small, 3. Medium, 4. Large, 5. X-Large
    
    # query price
    price = menu["size_price"][size]
    
    # update pizza_order, add size and price
    update_order(event["order_id"], size, price, datetime.now().strftime("%m-%d-%Y@%H:%M:%S"))
    
    returnMsg = {
        "Message" : "Your order costs $" + price + ". We will email you when the order is ready. Thank you!"
    }

    return returnMsg
