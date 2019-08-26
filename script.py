from newscheck.core import find_bad_articles 
from newscheck.util import check_article, StockQuotesCheck
from newscheck.archive import S3Archive
from newscheck import config, stock

if __name__ == "__main__":
    def is_stock_quotes(lines):
        return check_article(lines, config.THRESHOLD, stock.TICKER_SYMBOLS)
    archive = S3Archive("pybay2019", config.PREFIX, config.REGION_NAME)
    print(list(find_bad_articles(archive, StockQuotesCheck(config.THRESHOLD, stock.TICKER_SYMBOLS))))
