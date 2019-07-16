import config
import boto3



def find_bad_articles_2(bucket_name):
    client = boto3.client('s3', config.get_access_key(), config.get_secret_key())
    paginator = client.get_paginator('list_objects')

    page_iterator = paginator.paginate(bucket_name)
    for page in page_iterator:
        for item in page['Contents']:
            key, sz = item['Key'], item['Size']
            # Do something here
