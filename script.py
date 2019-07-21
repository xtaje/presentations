from __future__ import print_function
#import config
import boto3
import io
import pprint

THRESHOLD = 0.1
with open("stock_symbols.txt") as fobj:
    STOCK_SYMBOLS=[line.strip() for line in fobj.readlines()]

pp = pprint.PrettyPrinter(indent=4)

def find_bad_articles(bucket_name, batch_size=100):
    client = boto3.client('s3', region_name="us-east-2")
    paginator = client.get_paginator('list_objects')
    operation_parameters = {'Bucket': bucket_name, 'Prefix': 'news'}
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        contents = page['Contents']
        for item in contents:
            key = item['Key']
            if key == "news/":
                continue

            buf = io.BytesIO()
            client.download_fileobj(bucket_name, key, buf)
            buf.seek(0)

            lines = (line.decode().strip() for line in buf.readlines())
            lines = list(filter(lambda x:x, lines)) # drop empty lines

            ct = 0
            limit = THRESHOLD * len(lines)
            while lines and ct < limit:
                line = lines.pop()
                first_word = line.split()[0]
                if first_word in STOCK_SYMBOLS:
                    ct += 1


            print(ct, key, limit)
            if ct > limit:
                yield key


if __name__ == "__main__":
    print(list(find_bad_articles("pybay2019")))
