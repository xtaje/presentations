from __future__ import print_function
import config
import boto3
import cStringIO

STOCK_SYMBOLS=["MMM", "GOOG", "NFLX"] # and so on ...
THRESHOLD = 0.5

def find_bad_articles(bucket_name, fetcher):

    for key, data in fetcher.items():
        words = buf.getvalue().split()

        limit = THRESHOLD * len(words)
        for w in words:
            if w in STOCK_SYMBOLS:
               limit -=1 

            if limit <= 0:
                yield key

class DataFetcher(object):
    def __init__(self, bucket_name, aws_key, aws_secret, batch_size=100):
        self._conn = boto3.resource('s3', aws_key, aws_secret)
        self._bucket = self._conn.Bucket(bucket_name)

    def items(self):
        buf = cStringIO.StringIO()
        for obj in self._bucket.objects.page_size(self._batch_size):
            yield key, obj.downloadfileobj(buf)
