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
    
    # query menu_id of this order
    orderJsonStr = callLambda('GetPizzaOrder', {"order_id":event["order_id"]})
    #orderJsonUnicode = json.loads(orderJsonStr)
    orderDic =  json.loads(orderJsonStr)
    
    # query size name of size number
    sizeJsonStr = callLambda('GetPizzaMenuSize', {"menu_id": orderDic["menu_id"]})
    sizeDic = json.loads(sizeJsonStr)
    size = sizeDic[event["input"]] # 1. Slide, 2. Small, 3. Medium, 4. Large, 5. X-Large
    
    # query price
    priceJson = callLambda('GetPizzaMenuPriceBySize', {"menu_id": orderDic["menu_id"], "size": size})
    price = json.loads(priceJson)
    
    # update pizza_order, add size and price
    updateParams = {
        "order_id" : event["order_id"],
        "update_key1" : "size",
        "update_value1" : size,
        "update_key2" : "price",
        "update_value2" : price
    }
    updateResult = callLambda('UpdatePizzaOrder2', updateParams)
    print "add size and price:" + updateResult
    
    returnMsg = {
        "Message" : "Your order costs $" + price + ". We will email you when the order is ready. Thank you!"
    }

    return returnMsg
