import boto3
import json
import decimal
import collections

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def callLambda(functionName, parameters):
    lambda_client = boto3.client('lambda')

    responseData = None
    try:
        response = lambda_client.invoke(
            FunctionName=functionName, 
            InvocationType='RequestResponse',
            Payload=json.dumps(parameters))
        responseData = response['Payload'].read()
    except Exception as e:
        print(e)
    else:
        print("call " + functionName + "() succeeded:")
        #print(responseData)
        return responseData

def query_item(table_name, key_name, key_value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name) 
    try:
        response = table.get_item(
            Key={key_name: key_value}
        )
    except Exception as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print(table_name + " GetItem succeeded:")
        #print(json.dumps(item, indent=4, cls=DecimalEncoder))
        return item

def lambda_handler(event, context):
    
    # query menu_id of this order
    order = query_item('pizza_order', 'order_id', event["order_id"])
    
    menu = query_item('pizza_menu', 'menu_id', order["menu_id"])
    selectionDic = {}
    for idx, val in enumerate(menu["selection"]):
        selectionDic[str(idx+1)] = val
    selection = selectionDic[event["input"]]
    
    # update selection
    updateResult = callLambda('UpdatePizzaOrder', {"order_id":event["order_id"], "update_key":"selection", "update_value":selection})
    print updateResult
    
    
    # query sizes string of menu
    sizeDic = {}
    for idx, val in enumerate(menu["size"]):
        sizeDic[str(idx+1)] = val

    amount = len(sizeDic)
    count = 1
    sizeStr = ''
    orderedSizeDic = collections.OrderedDict(sorted(sizeDic.items()))
    for key in orderedSizeDic:
        sizeStr += key + ". " + orderedSizeDic[key]
        if(count != amount):
            sizeStr += ", "
        count += 1
    
    returnMsg = {
        "Message" : "Which size do you want? " + sizeStr
    }

    return returnMsg
