import boto3,os,json

#connect to S3
def connect():
    s3 = boto3.resource('s3',
        aws_access_key_id='PUT AWS SESSION KEY',
        aws_secret_access_key='AWS ACCESS KEY')
    return s3

def create_bucket(s3,name):
    s3.create_bucket(Bucket=name)
    bucket = s3.Bucket(name)
    bucket.Acl().put(ACL='public-read')

def set_bucket_policy(bucket_name):
    s_cli = boto3.client('s3',
        aws_access_key_id='ACCESS KEY ID',
        aws_secret_access_key='XXX')
    bucket_policy = {
                    'Version': '2012-10-17',
                    'Statement': [{
                        'Sid': 'AddPerm',
                        'Effect': 'Allow',
                        'Principal': '*',
                        'Action': ['s3:GetObject'],
                        'Resource': "arn:aws:s3:::%s/*" % bucket_name
                    }]
                    }
    bucket_policy = json.dumps(bucket_policy)
    s_cli.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

def get_bucketname(s3):
    bucket_names = []
    for bucket in s3.buckets.all():
        bucket_names.append(bucket.name)
    print("bucket list : ", bucket_names)
    return(bucket_names[0])

def get_itemsin_bucket(bucket_name,s3):
    items = []
    bucket = s3.Bucket(bucket_name)
    for key in bucket.objects.all():
        items.append(key.key)
    print("items in bucket : ", items)
    return(items)

def upload_intobucket(localfilepath, bucket, filename,s3):
    # # Upload a new file to bucket
    data = open(localfilepath, 'rb')
    s3.Bucket(bucket).put_object(Key=filename, Body=data)
    return filename
