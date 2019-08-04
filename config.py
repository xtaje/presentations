_STOCK_SYMBOLS=None

def stock_symbols():
    global _STOCK_SYMBOLS
    if _STOCK_SYMBOLS is None:
        with open("stock_symbols.txt") as fobj:
            _STOCK_SYMBOLS=[line.strip() for line in fobj.readlines()]
    return _STOCK_SYMBOLS

REGION_NAME="us-east-2"
THRESHOLD = 0.5
PREFIX="news"
BATCH_SIZE=100
