from __future__ import print_function
import config
import boto3
import cStringIO
from itertools import chain

STOCK_SYMBOLS=["MMM", "GOOG", "NFLX"] # and so on ...
THRESHOLD = 0.5

def find_bad_articles(bucket_name, batch_size, aws_key, aws_secret): 
    objects = s3.resource(aws_key, aws_secret)
                .bucket(bucket_name)
                .objects
                .page_size(batch_size)
    return map(is_blacklisted, fetch_objects(objects))

def is_blacklisted(key, text):
    words = text.split()
    limit = THRESHOLD * len(words)
    for w in words:
        if w in STOCK_SYMBOLS:
           limit -=1 

        if limit <= 0:
            yield key

def fetch_objects(objects, batch_size, s3):
    for obj in objects:
        buf = cStringIO.StringIO()
        obj.downloadfileobj(buf)
        yield obj.key, buf.getvalue()
