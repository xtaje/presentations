import boto3
import io
import config


def detect_bad_article(lines, threshold, stock_symbols):
    lines = list(filter(lambda x:x, lines))
    limit = threshold * len(lines)
    while lines and limit:
        line = lines.pop()
        first_word = line.split()[0]
        if first_word in stock_symbols:
            limit -= 1

    return limit <= 0

def find_bad_articles(bucket_name, is_bad_article):
    client = boto3.client('s3', region_name=config.REGION_NAME)
    paginator = client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=config.PREFIX)
    for page in page_iterator:
        for item in page['Contents']:
            key = item['Key']
            if key == f"{config.PREFIX}/": #ignore root
                continue

            buf = io.BytesIO()
            client.download_fileobj(bucket_name, key, buf)

            buf.seek(0)
            lines = (line.decode().strip() for line in buf.readlines())

            if is_bad_article(lines):
                yield key


if __name__ == "__main__":
    def is_bad_article(lines):
        return detect_bad_article(lines, 
                threshold=config.THRESHOLD,
                stock_symbols=config.stock_symbols()
                )
    print(list(find_bad_articles("pybay2019", is_bad_article)))
