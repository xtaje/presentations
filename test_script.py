import unittest
from unittest import mock
from mock import MagicMock
from . script import find_bad_articles

class TestBadArticleFinder(unittest.TestCase):
    @mock.patch("presentations.script.get_file")
    @mock.patch("presentations.script.get_pages")
    def test_find_bad_articles_mocked(self, get_pages_mock, get_file_mock):
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

    def test_find_bad_articles(self):
        bucket_name = "pybay2019"

        bad_articles = list(find_bad_articles(bucket_name))
        self.assertEqual(1, len(bad_articles))
        self.assertEqual("news/3.txt", bad_articles[0])
