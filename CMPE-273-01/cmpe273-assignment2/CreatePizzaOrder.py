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

    # insert new order
    responseData = callLambda('PutPizzaOrderTest1', event)
    print responseData
    
    # query selection
    responseData = callLambda('GetPizzaMenuSelection', {"menu_id":event["menu_id"]})
    selectionDic = json.loads(responseData)
    
    responseMsg = ""
    amount = len(selectionDic)
    count = 1
    for key in selectionDic:
        responseMsg = responseMsg + key + ". " + selectionDic[key]
        if(count != amount):
            responseMsg += ", "
        count += 1
    print responseMsg
    msgDic = {
        "Message" : "Hi " + event["customer_name"] + ", please choose one of these selection: " + responseMsg
    }
    return msgDic