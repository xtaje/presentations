import unittest
from unittest import mock
from newscheck.core import find_bad_articles

class TestBadArticleFinder(unittest.TestCase):
    def test_find_bad_articles(self):

        data = {
            "good.txt": ["lorem ipsum dolorum"],
            "bad.txt": ["i am the bad article"]
        }

        def check(lines):
            return lines[0] == "i am the bad article"

        bad_articles = list(find_bad_articles(data.items(), check))
        self.assertEqual(1, len(bad_articles))
        self.assertEqual("bad.txt", bad_articles[0])


