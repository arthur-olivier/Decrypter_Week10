import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):

    shaHash= event['pathParameters']['shaHash']
    #shaHash = '8b20c87e909d13f9a12c0f1b9a540b6b3714c003'
    password=''
    statusCode= 200

    
    
    data = s3.select_object_content(
        Bucket='decrypter-bucket',
        Key='data.csv',
        ExpressionType='SQL',
        Expression=f"SELECT * FROM s3object s where s.shaHash = '{shaHash}'",
        InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}, 'CompressionType': 'NONE'},
        OutputSerialization = {'CSV': {}},
    )
    
    for event in data['Payload']:
        if 'Records' in event:
            password = event['Records']['Payload'].decode('utf-8')
    
    x=['No found','No found']
    if password=="":
        statusCode=404
    else :
        x=password.split(",") 
    
    return {
        'statusCode': statusCode,
        'body': "hash : " + x[0] + "  , password : "+ x[1]
    }
