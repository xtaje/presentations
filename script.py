import boto3
import io
from fetcher import ArticleFetcher

with open("stock_symbols.txt") as fobj:
    STOCK_SYMBOLS=[line.strip() for line in fobj.readlines()]

REGION_NAME="us-east-2"
THRESHOLD = 0.5
PREFIX="news"

def find_bad_articles(fetcher):
    for key in fetcher.get_keys():
        lines = fetcher.download_key(key)

        limit = THRESHOLD * len(lines)
        while lines and limit:
            line = lines.pop()
            first_word = line.split()[0]
            if first_word in STOCK_SYMBOLS:
                limit -= 1

        if limit <= 0:
            yield key

if __name__ == "__main__":
    client = boto3.client('s3', region_name=REGION_NAME)
    fetcher = ArticleFetcher(client, "pybay2019", "news")
    print(list(find_bad_articles(fetcher)))
