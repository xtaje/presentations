import boto3
import io
import config
from util import check_article
from s3 import S3Archive

def find_bad_articles(bucket_name):
    archive = S3Archive(bucket_name, 
                        config.PREFIX,
                        config.REGION_NAME)
    for key in archive.get_keys():
        lines = archive.get_file(key)
        if check_article(lines, config.THRESHOLD, config.STOCK_SYMBOLS):
            yield key


if __name__ == "__main__":
    print(list(find_bad_articles("pybay2019")))
