import ipaddress
import json
import maxminddb
import os

def handler(event, context):

    try:
        ip = ipaddress.ip_address(event['rawQueryString'])
        ip = str(event['rawQueryString'])
    except ValueError:
        ip = ipaddress.ip_address(event['requestContext']['http']['sourceIp'])
        ip = str(event['requestContext']['http']['sourceIp'])

    try:
        with maxminddb.open_database('ipinfo_lite.mmdb') as reader:
            response = reader.get(ip)
            asn = response['asn']
            as_domain = response['as_domain']
            as_name = response['as_name']
            continent = response['continent']
            continent_code = response['continent_code']
            country = response['country']
            country_code = response['country_code']
    except:
        asn = None
        as_domain = None
        as_name = None
        continent = None
        continent_code = None
        country = None
        country_code = None

    f = open('ipinfo_lite.updated', 'r')
    updated = f.read()
    f.close()

    desc = 'IP address data powered by IPinfo, available from https://ipinfo.io.'

    code = 200
    msg = {
        'ip':str(ip),
        'geo': {
            'country':country,
            'country_code':country_code,
            'continent':continent,
            'continent_code':continent_code
        },
        'asn': {
            'id': asn,
            'name': as_name,
            'domain': as_domain
        },
        'attribution':desc,
        'ipinfo_lite.mmdb':updated,
        'region': os.environ['AWS_REGION']
    }

    return {
        'statusCode': code,
        'body': json.dumps(msg, indent = 4)
    }