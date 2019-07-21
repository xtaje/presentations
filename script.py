import boto3
import io

with open("stock_symbols.txt") as fobj:
    STOCK_SYMBOLS=[line.strip() for line in fobj.readlines()]

REGION_NAME="us-east-2"
THRESHOLD = 0.5
PREFIX="news"
BATCH_SIZE=100

def find_bad_articles(bucket_name):
    client = boto3.client('s3', region_name=REGION_NAME)
    paginator = client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=PREFIX)
    for page in page_iterator:
        for item in page['Contents']:
            key = item['Key']
            if key == f"{PREFIX}/": #ignore root
                continue

            buf = io.BytesIO()
            client.download_fileobj(bucket_name, key, buf)

            # Decode and drop empty lines
            buf.seek(0)
            lines = (line.decode().strip() for line in buf.readlines())
            lines = list(filter(lambda x:x, lines))

            limit = THRESHOLD * len(lines)
            while lines and limit:
                line = lines.pop()
                first_word = line.split()[0]
                if first_word in STOCK_SYMBOLS:
                    limit -= 1

            if limit <= 0:
                yield key


if __name__ == "__main__":
    print(list(find_bad_articles("pybay2019")))
