import boto3
import io
import config


def find_bad_articles(article_source, predicate):
    for key in article_source.get_keys():
        lines = article_source.get_file(key)
        if predicate(lines):
            yield key


if __name__ == "__main__":
    client = boto3.client('s3', region_name=config.REGION_NAME)
    policy = StockArticlePolicy(config.threshold, config.get_stock_symbols())
    article_source = S3Fetcher(client, "pybay2019", "config.PREFIX")
    print(list(find_bad_articles(article_source, policy))



