import unittest
from unittest import mock
from mock import MagicMock, call
from newscheck.core import find_bad_articles

class TestBadArticleFinder(unittest.TestCase):
    @mock.patch("newscheck.core.get_file")
    @mock.patch("newscheck.core.get_pages")
    @mock.patch("newscheck.core.boto3.client")
    def test_find_bad_articles_mocked(self, client_mock, get_pages_mock, get_file_mock):
        mock_client = MagicMock(name="mock s3 client")
        client_mock.return_value = mock_client
        bucket_name = "my_bucket"
        page_stub = [{
                "Contents": [
                    { "Key": 'news/'},
                    { "Key": 'news/good.txt'},
                    { "Key": 'news/bad.txt'}
                    ]
        }]
        get_pages_mock.return_value = page_stub

        file_stubs = [
            "lorem ipsum dolorum\n foo baz bar biz\n hello world".split('\n'),
            "MSFT 99.32\n BAC 22.3\n F 33.2\n".split('\n'),
        ]
        get_file_mock.side_effect = file_stubs 

        bad_articles = list(find_bad_articles(bucket_name))
        self.assertEqual(1, len(bad_articles))
        self.assertEqual("news/bad.txt", bad_articles[0])

        self.assertEqual([call(mock_client, "my_bucket", "news")], 
                          get_pages_mock.mock_calls)

        self.assertEqual([
                call(mock_client,"my_bucket", "news/good.txt"),
                call(mock_client,"my_bucket", "news/bad.txt")
            ],
            get_file_mock.mock_calls
        )

    def test_find_bad_articles(self):
        bucket_name = "pybay2019"

        bad_articles = list(find_bad_articles(bucket_name))
        self.assertEqual(1, len(bad_articles))
        self.assertEqual("news/3.txt", bad_articles[0])
