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
    
    initialdoc = result1

    # translate -------------------------------
    #1 - Recover text to translate
    print('1 - Recover text to translate')
    print('result1 : ' + str(result1['Item']))
    
    texto = ''
    result1 = str(result1['Item']).replace("\'", "\"")
 
    result1 = str(result1).replace('True','"True"')
    result1 = str(result1).replace('False','False"')
    result1 = str(result1).replace('Decimal("','"Decimal(\'')
    result1 = str(result1).replace('")}','\')"}')
 
    print('result1 escapado y parseado: ' + str(result1))
     
    json_object = json.loads(str(result1))
    pairs = json_object.items()

    for key, value in pairs:
       if key == 'text' : texto = value
    
    if texto == '':  
        print('NO ha encontrado el campo text en el registro desde BBDD.')
        return
    
    #2 - translate text
    
    print('texto a traducir : ' + str(texto))
    
    textotraducido =''
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
    if  event['pathParameters']['language'] == 'FR':
        textotraducido = translate.translate_text(Text=texto, SourceLanguageCode="en", TargetLanguageCode="fr")
    else :
        textotraducido = translate.translate_text(Text=texto, SourceLanguageCode="en", TargetLanguageCode="es")
    
    print('texto traducido : ' + str(textotraducido))
        
    #3 - change language 
    
    result = str(initialdoc).replace(str(texto), str(textotraducido))
    print('result : ' + str(result))
        
        
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result,
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
