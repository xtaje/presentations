import unittest
import mock



class TestBadArticleFinder(unittest.TestCase):
    @mock.patch("script.boto3", autospec=True)
    def test_find_bad_articles(self, mock_boto3):
        mock_boto3.resource.Bucket.objects.page_size.return_value = # ?. @$!!?! I give up!

        bad_articles = list(find_bad_articles("my_bucket"))

        # assert something here



