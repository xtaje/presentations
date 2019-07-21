import unittest
from script import find_bad_articles
from moto import mock_s3
import boto3


class TestBadArticleFinder(unittest.TestCase):
    @mock_s3
    def test_find_bad_articles(self):
        bucket_name = "my_bucket"

        conn = boto3.resource('s3', region_name='us-east-2')
        bucket = conn.create_bucket(Bucket="my_bucket")
        bucket.put_object(Key="news/good_article", 
            Body="Prince Archie and the Queen ...")

        bucket.put_object(Key="news/bad_article", 
            Body="TSLA -13.0%\nBAC 0.22%\nXOM -1.01%\nNFLX -2.0%\nV 0.9%\nAMD 0.4%")

        bad_articles = list(find_bad_articles(bucket_name))
        self.assertEqual("news/bad_article", bad_articles[0])




