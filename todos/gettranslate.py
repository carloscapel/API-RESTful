import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def gettranslate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result1 = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # translate -------------------------------
    #1 - Recover text to translate
    print  "1 - Recover text to translate"
    print   "result1 : " + result1
    
    texto = ''
    json_object = json.loads(result1)
    pairs = json_object.items()

    for key, value in pairs:
       if (key == 'text' ) texto = value
    
    if texto == ''  
        print("NO ha encontrado el campo text en el registro desde BBDD.")
        return
    
    #2 - translate text
    translate = boto3.client(service_name='translate', region_name='region', use_ssl=True)
    if ( event['pathParameters']['language'] = 'FR')
        result1 = translate.translate_text(Text=texto, SourceLanguageCode="en", TargetLanguageCode="fr")
    else
        result1 = translate.translate_text(Text=texto, SourceLanguageCode="en", TargetLanguageCode="es")
    print("result1 : " + result1)
        
    #3 - change language 
    result = string.replace(texto, result1)
    print("result : " + result)
        
        
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
