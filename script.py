from __future__ import print_function
import config
import boto3
import cStringIO

STOCK_SYMBOLS=["MMM", "GOOG", "NFLX"] # and so on ...
THRESHOLD = 0.5

def find_bad_articles(bucket_name, predicate, batch_size=100):
    s3 = boto3.resource('s3', config.aws_key, config.aws_secret)
    objects = s3.Bucket(bucket_name).objects
    for obj in objects.page_size(batch_size):
        buf = cStringIO.StringIO()
        obj.downloadfileobj(buf)

        if predicate(buf.get_value()):
            yield key



def is_blacklisted(text, threshold=0.5):
    words = text.split()
    limit = threshold * len(words)
    for w in words:
        if w in STOCK_SYMBOLS:
           limit -=1 

        if limit <= 0:
            return True
    return False
