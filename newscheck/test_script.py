import unittest
from unittest import mock
from mock import MagicMock
from newscheck.core import find_bad_articles
from newscheck.archive import S3Archive

class TestBadArticleFinder(unittest.TestCase):
    def test_find_bad_articles(self):

        prefix = "news"
        fake_files = {
            f"{prefix}/good.txt": ["lorem ipsum dolorum"],
            f"{prefix}/bad.txt": ["i am the bad article"]
        }
        page = { "Contents": [
                        { "Key": f"{prefix}/"},
                        { "Key": f"{prefix}/good.txt"},
                        { "Key": f"{prefix}/bad.txt"}
               ]}

        class FakeArchive(S3Archive):
            def __init__(self):
                super(FakeArchive, self).__init__(
                        bucket_name="dummy_bucket", 
                        prefix=prefix, 
                        client=MagicMock())

            def get_pages(self):
                return [page]

            def get_file(self, key):
                return fake_files[key]

        def check(lines):
            return lines[0] == "i am the bad article"

        bad_articles = list(find_bad_articles(FakeArchive(), check))
        self.assertEqual(1, len(bad_articles))
        self.assertEqual("news/bad.txt", bad_articles[0])

