import boto3 
import newscheck.config as config
import newscheck.stock as stock
from newscheck.util import get_pages, keys_from, get_file, check_article



def find_bad_articles(bucket_name):
    client = boto3.client('s3', region_name=config.REGION_NAME)

    for page in get_pages(client, bucket_name, config.PREFIX):
        for key in keys_from(page):
            lines = get_file(client, bucket_name, key)
            if check_article(lines, config.THRESHOLD, stock.TICKER_SYMBOLS):
                yield key


