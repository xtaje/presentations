import unittest
import mock
from script import find_bad_articles
import boto3


class TestBadArticleFinder2(unittest.TestCase):
    @mock.patch("script.download_key")
    @mock.patch("script.get_keys")
    def test_find_bad_articles(self, mock_get_keys, mock_download_key):
        bucket_name = "my_bucket"

        keys = ["news/good_article", "news/bad_article"]
        def _get_keys(*args, **kwargs):
            yield keys[0]
            yield keys[1]
        bodies = ["Prince Archie and the Queen ...".split('\n'),
            "TSLA -13.0%\nBAC 0.22%\nXOM -1.01%\nNFLX -2.0%\nV 0.9%\nAMD 0.4%".split("\n")]

        mock_get_keys.side_effect = _get_keys
        mock_download_key.side_effect = bodies

        bad_articles = list(find_bad_articles(bucket_name))
        print(bad_articles)
        self.assertEqual("news/bad_article", bad_articles[0])

