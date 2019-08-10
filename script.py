import boto3
import io
import config

def find_bad_articles(bucket_name):
    client = boto3.client('s3', region_name=config.REGION_NAME)
    for page in get_pages(client, bucket_name, config.PREFIX):
        for item in page['Contents']:
            key = item['Key']
            if key == f"{config.PREFIX}/": #ignore root
                continue

            lines = get_file(client, bucket_name, key)

            if check_article(lines, config.THRESHOLD, config.STOCK_SYMBOLS):
                yield key


if __name__ == "__main__":
    print(list(find_bad_articles("pybay2019")))
