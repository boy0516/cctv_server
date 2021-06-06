import json
import pymysql
import os
  
db_config = json.loads(os.environ['db_config'])

conn = pymysql.connect(**db_config)
cursor = conn.cursor()


def lambda_handler(event, context):
    # TODO implement
    
    cctvname = event["cctvname"]
    situation = event["situation"]
    s3_url = event["s3_url"]
    
    sql = "INSERT INTO cctvlog (cctvname, situation, s3_url) values ('%s', '%s', '%s')"
    cursor.execute(sql % (cctvname, situation, s3_url))
    conn.commit()
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
