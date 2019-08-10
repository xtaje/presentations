import boto3
import io
import config
from util import check_article
from s3 import S3Archive

def find_bad_articles(archive, predicate):
    for key in archive.get_keys():
        lines = archive.get_file(key)
        if predicate(lines):
            yield key


if __name__ == "__main__":
    def is_stock_quotes(lines):
        return check_article(lines, config.THRESHOLD, config.STOCK_SYMBOLS)

    client = boto3.client('s3', region_name=config.REGION_NAME)

    archive = S3Archive("pybay2019", 
                        config.PREFIX,
                        client)

    print(list(find_bad_articles(archive, is_stock_quotes)))
