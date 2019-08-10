import boto3
import config
import io

class S3Archive(object):
    def __init__(self, bucket_name, prefix, region_name):
        """Ctor"""
        self.client = boto3.client('s3', region_name=region_name)
        self.bucket_name = bucket_name
        self.prefix = prefix

    def get_keys(self):
        """Get an iterable of keys"""
        for page in self.get_pages():
            for key in self.keys_from(page):
                yield key

    def get_file(self, key):
        """Get a file and return as non-empty lines"""
        buf = io.BytesIO()
        self.client.download_fileobj(self.bucket_name, key, buf)
    
        # Decode and drop empty lines
        buf.seek(0)
        lines = (line.decode().strip() for line in buf.readlines())
        return list(filter(lambda x:x, lines))

    def get_pages(self):
        """Get a paginated key list"""
        paginator = self.client.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix=self.prefix)
        return page_iterator
    
    def keys_from(self, page):
        """Parse keys from page response"""
        for item in page['Contents']:
            key = item['Key']
            if key == f"{self.prefix}/": #ignore root
                continue
            yield key
