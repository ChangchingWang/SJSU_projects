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

def lambda_handler(event, context):

    # update pizza_order, add selection
    updateResult = callLambda('UpdatePizzaOrder', event)
    print updateResult
    
    # query menu_id of this order
    orderJsonStr = callLambda('GetPizzaOrder', {"order_id":event["order_id"]})
    #orderJsonUnicode = json.loads(orderJsonStr)
    orderDic =  json.loads(orderJsonStr)
    
    # query sizes string of menu
    sizeJsonStr = callLambda('GetPizzaMenuSize', {"menu_id": orderDic["menu_id"]})
    sizeDic = json.loads(sizeJsonStr)
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
