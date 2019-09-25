from newscheck.core import find_bad_articles 
from newscheck.util import check_article, StockQuotesCheck
from newscheck.archive import S3Archive
from newscheck import config, stock

import boto3

if __name__ == "__main__":
    def is_stock_quotes(key_and_lines):
        return check_article(key_and_lines[1], config.THRESHOLD, stock.TICKER_SYMBOLS)

    client = boto3.client('s3', region_name=config.REGION_NAME)
    archive = S3Archive("pybay2019", config.PREFIX, client)

    found_articles = filter(is_stock_quotes, archive.items())
    bad_keys = map(lambda key_and_lines: key_and_lines[0], found_articles)
    print(list(bad_keys))
