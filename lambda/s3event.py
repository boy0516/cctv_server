import json
import requests
import boto3
import os
from urllib import parse

def lambda_handler(event, context):
    # TODO implement
    
    # s3키는 람다의 환경변수에 저장
    s3 = boto3.client('s3',
                    aws_access_key_id=os.environ['aws_access_key_id'],
                    aws_secret_access_key=os.environ['aws_secret_access_key'],
                    region_name='eu-central-1'
                    )
                    
    sns = boto3.client('sns',
                    aws_access_key_id=os.environ['aws_access_key_id'],
                    aws_secret_access_key=os.environ['aws_secret_access_key'],
                    region_name='eu-central-1'
                    )
    
    
    filename = parse.unquote(event["Records"][0]["s3"]["object"]["key"])
    print(type(filename))
    
    s3.put_object_acl(
        Bucket = os.environ['Bucket'],
        ACL = 'public-read',
        Key = filename
    )
    
    name_source = filename.split('.')[0]
    print(name_source)
    a = name_source.split('_')
    print(a)
    cctvname = a[0]
    print(cctvname)
    situation = a[2]
    print(situation)
    
    if (situation=="폭행") or  (situation=="흡연") :
        print('sns 잘뜨나')
        sns.publish(PhoneNumber='+821028484812', Message=situation+'감지')
        print('sns 끝')
    
    s3_url = 'https://yangjae-team05-s3.s3.eu-central-1.amazonaws.com/'+filename
    print(s3_url)
    insert_data = json.dumps({
        "cctvname": cctvname,
        "situation": situation,
        "s3_url": s3_url
    })
    print(type(insert_data))
    res = requests.post(url='https://3wl2br3yq5.execute-api.eu-central-1.amazonaws.com/rds-insert/db/insert',
                        data=insert_data, headers={'Content-Type': 'application/json'})
    return {
        'statusCode': 200,
        'body': json.dumps(res.text)
    }