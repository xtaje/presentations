import boto3
import io
import config

def get_client():
    return boto3.client('s3', region_name=config.REGION_NAME)

def get_pages(bucket_name, prefix):
    client = get_client()
    paginator = client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    return page_iterator

def get_file(bucket_name, key):
    client = get_client()
    buf = io.BytesIO()
    client.download_fileobj(bucket_name, key, buf)

    # Decode and drop empty lines
    buf.seek(0)
    lines = (line.decode().strip() for line in buf.readlines())
    lines = list(filter(lambda x:x, lines))
    return lines

def get_keys_from_page(page):
    for item in page['Contents']:
        key = item['Key']
        if key == f"{config.PREFIX}/": #ignore root
            continue
        yield key

def get_keys(bucket_name, prefix):
    page_iterator = get_pages(bucket_name, prefix)
    for page in page_iterator:
        for key in get_keys_from_page(page):
            yield key

def find_bad_articles(bucket_name):
    for key in get_keys(bucket_name, config.PREFIX):
        lines = get_file(bucket_name, key)

        limit = config.THRESHOLD * len(lines)
        while lines and limit:
            line = lines.pop()
            first_word = line.split()[0]
            if first_word in config.stock_symbols():
                limit -= 1

        if limit <= 0:
            yield key


if __name__ == "__main__":
    print(list(find_bad_articles("pybay2019")))
