import boto3
import json
import os
import zipfile

def handler(event, context):

    s3_client = boto3.client('s3')

    print("Copying ipinfo_lite.mmdb")

    with open('/tmp/ipinfo_lite.mmdb', 'wb') as f:
        s3_client.download_fileobj(os.environ['S3_BUCKET'], 'ipinfo_lite.mmdb', f) 
    f.close()

    print("Copying ipinfo_lite.updated")

    with open('/tmp/ipinfo_lite.updated', 'wb') as f:
        s3_client.download_fileobj(os.environ['S3_BUCKET'], 'ipinfo_lite.updated', f) 
    f.close()

    print("Copying find.py")

    with open('/tmp/find.py', 'wb') as f:
        s3_client.download_fileobj(os.environ['S3_BUCKET'], 'find.py', f) 
    f.close()

    print("Packaging ipinfo.zip")

    with zipfile.ZipFile('/tmp/ipinfo.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:

        zipf.write('/tmp/ipinfo_lite.mmdb','ipinfo_lite.mmdb')
        zipf.write('/tmp/ipinfo_lite.updated','ipinfo_lite.updated')
        zipf.write('/tmp/find.py','find.py')

    zipf.close()

    response = s3_client.upload_file('/tmp/ipinfo.zip',os.environ['S3_BUCKET'],'ipinfo.zip')

    s3_client = boto3.client('s3', region_name = 'us-east-1')

    response = s3_client.upload_file('/tmp/ipinfo.zip',os.environ['S3_USE1'],'ipinfo.zip')
 
    s3_client = boto3.client('s3', region_name = 'us-west-2')

    response = s3_client.upload_file('/tmp/ipinfo.zip',os.environ['S3_USW2'],'ipinfo.zip')

    client = boto3.client('lambda', region_name = 'us-east-1')

    print("Updating "+os.environ['LAMBDA_FUNCTION_USE1'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_FUNCTION_USE1'],
        S3Bucket = os.environ['S3_USE1'],
        S3Key = 'ipinfo.zip'
    )

    client = boto3.client('lambda', region_name = 'us-west-2')

    print("Updating "+os.environ['LAMBDA_FUNCTION_USW2'])

    response = client.update_function_code(
        FunctionName = os.environ['LAMBDA_FUNCTION_USW2'],
        S3Bucket = os.environ['S3_USW2'],
        S3Key = 'ipinfo.zip'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }