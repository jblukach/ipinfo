import base64
import boto3
import datetime
import json
import os
import requests

def handler(event, context):

    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    day = datetime.datetime.now().strftime('%d')
    hour = datetime.datetime.now().strftime('%H')
    now = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    secret = boto3.client('secretsmanager')

    getsecret = secret.get_secret_value(
        SecretId = os.environ['SECRET_MGR_ARN']
    )

    token = json.loads(getsecret['SecretString'])

    url = f'https://ipinfo.io/data/ipinfo_lite.mmdb?_src=frontend&token={token["api"]}'

    response = requests.get(url)

    with open(f'/tmp/ipinfo_lite.mmdb', 'wb') as f:
        f.write(response.content)
    f.close()

    with open(f'/tmp/ipinfo_lite.updated', 'w') as f:
        f.write(now)
    f.close()

    s3 = boto3.client('s3')
    
    response = s3.upload_file('/tmp/ipinfo_lite.mmdb',os.environ['S3_STAGED'],'ipinfo_lite.mmdb')
    response = s3.upload_file('/tmp/ipinfo_lite.mmdb',os.environ['S3_RESEARCH'],year+'/'+month+'/'+day+'/'+hour+'/ipinfo_lite.mmdb')
    response = s3.upload_file('/tmp/ipinfo_lite.updated',os.environ['S3_STAGED'],'ipinfo_lite.updated')
    response = s3.upload_file('/tmp/ipinfo_lite.updated',os.environ['S3_RESEARCH'],year+'/'+month+'/'+day+'/'+hour+'/ipinfo_lite.updated')

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }