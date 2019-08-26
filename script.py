from newscheck.core import find_bad_articles 
from newscheck.util import check_article, StockQuotesCheck
from newscheck import config, stock

if __name__ == "__main__":
    def is_stock_quotes(lines):
        return check_article(lines, config.THRESHOLD, stock.TICKER_SYMBOLS)
    print(list(find_bad_articles("pybay2019", StockQuotesCheck(config.THRESHOLD, stock.TICKER_SYMBOLS))))
