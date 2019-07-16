from __future__ import print_function
import config
import boto3
import cStringIO

STOCK_SYMBOLS=["MMM", "GOOG", "NFLX"] # and so on ...
THRESHOLD = 0.5

def find_bad_articles(bucket_name, batch_size): 
    fetched = fetch_objects(bucket_name, batch_size)
    return _find_bad_articles(bucket_name, fetched)

def _find_bad_articles(bucket_name, fetched_objects):
    for key, text in fetched_objects:
        words = text.split()
        limit = THRESHOLD * len(words)
        for w in words:
            if w in STOCK_SYMBOLS:
               limit -=1 

            if limit <= 0:
                yield key

def fetch_objects(bucket_name, batch_size):
    s3 = boto3.resource('s3', config.aws_key, config.aws_secret)
    objects = s3.Bucket(bucket_name).objects
    for obj in objects.page_size(batch_size)
        buf = cStringIO.StringIO()
        obj.downloadfileobj(buf)
        yield obj.key, buf.getvalue()
