from newscheck.core import find_bad_articles 
from newscheck.util import check_article, StockQuotesCheck
from newscheck.archive import S3Archive
from newscheck import config, stock

import boto3

if __name__ == "__main__":
    def is_stock_quotes(lines):
        return check_article(lines, config.THRESHOLD, stock.TICKER_SYMBOLS)
    client = boto3.client('s3', region_name=config.REGION_NAME)
    archive = S3Archive("pybay2019", config.PREFIX, client)
    print(list(find_bad_articles(archive, StockQuotesCheck(config.THRESHOLD, stock.TICKER_SYMBOLS))))
