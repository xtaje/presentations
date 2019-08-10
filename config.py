STOCK_SYMBOLS=None
if STOCK_SYMBOLS is None:
    with open("stock_symbols.txt") as fobj:
        STOCK_SYMBOLS=[line.strip() for line in fobj.readlines()]

REGION_NAME="us-east-2"
THRESHOLD = 0.5
PREFIX="news"
BATCH_SIZE=100
