import json

def handler(event, context):

    return {
        'statusCode': 200,
        'body': json.dumps('IP address data powered by IPinfo, available from https://ipinfo.io.')
    }