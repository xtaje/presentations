import unittest
from moto import mock_s3


class TestBadArticleFinder(unittest.TestCase):
    @mock_s3
    def test_find_bad_articles(self):
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket="my_bucket")

        bucket_name = "my_bucket"

        conn.put_object(Bucket=bucket_name, Key="good_article", 
            Body="Prince Archie and the Queen ...")

        conn.put_object(Bucket=bucket_name, Key="bad_article", 
            Body=TSLA -13.0% AAPL 0.22% XOM -1.01% GOOG -2.0% V 0.9% TSLA"

        bad_articles = list(find_bad_articles(bucket_name))
        self.assertEqual(1, len(bad_articles))
        self.assert("bad_article", bad_articles[0])




