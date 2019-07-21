import io

with open("stock_symbols.txt") as fobj:
    STOCK_SYMBOLS=[line.strip() for line in fobj.readlines()]

REGION_NAME="us-east-2"
THRESHOLD = 0.5
PREFIX="news"

def find_bad_articles(bucket_name, boto3):
    client = boto3.client('s3', region_name=REGION_NAME)

    for key in get_keys(client, bucket_name):
        lines = download_key(client, bucket_name, key)

        limit = THRESHOLD * len(lines)
        while lines and limit:
            line = lines.pop()
            first_word = line.split()[0]
            if first_word in STOCK_SYMBOLS:
                limit -= 1

        if limit <= 0:
            yield key

def get_keys(client, bucket_name):
    pages = get_pages(client, bucket_name)
    for page in pages:
        for item in page['Contents']:
            key = item['Key']
            if key == f"{PREFIX}/": #ignore root
                continue
            else:
                yield key

def get_pages(client, bucket_name):
    paginator = client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=PREFIX)
    return page_iterator

def download_key(client, bucket_name, key):
    buf = io.BytesIO()
    client.download_fileobj(bucket_name, key, buf)
    buf.seek(0)
    
    lines = (line.decode().strip() for line in buf.readlines())
    lines = list(filter(lambda x:x, lines))
    return lines

if __name__ == "__main__":
    import boto3
    print(list(find_bad_articles("pybay2019", boto3)))
