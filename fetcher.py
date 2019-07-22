import io

class ArticleFetcher(object):
    def __init__(self, client, bucket_name, prefix):
        self._client = client
        self._bucket_name = bucket_name
        self._prefix = prefix

    def get_keys(self):
        pages = self.get_pages()
        for page in pages:
            for item in page['Contents']:
                key = item['Key']
                if key == f"{self._prefix}/": #ignore root
                    continue
                else:
                    yield key
    
    def get_pages(self):
        paginator = self._client.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=self._bucket_name, Prefix=self._prefix)
        return page_iterator
    
    def download_key(self, key):
        buf = io.BytesIO()
        self._client.download_fileobj(self._bucket_name, key, buf)
        buf.seek(0)
        
        lines = (line.decode().strip() for line in buf.readlines())
        lines = list(filter(lambda x:x, lines))
        return lines

    def items(self):
        for key in self.get_keys():
            lines = self.download_key(key)
            yield key, lines
