


class S3Fetcher(object):
    def __init__(self, client, bucket_name, prefix):
        self._client=client
        self._bucket_name
        self._prefix=prefix

    def get_pages(self):
        paginator = self._client.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=self._bucket_name, Prefix=self._prefix)
        return page_iterator

    def get_file(self, key):
        buf = io.BytesIO()
        self._client.download_fileobj(self._bucket_name, key, buf)

        # Decode and drop empty lines
        buf.seek(0)
        lines = (line.decode().strip() for line in buf.readlines())
        lines = list(filter(lambda x:x, lines))
        return lines

    @staticmethod
    def get_keys_from_page(page):
        for item in page['Contents']:
            key = item['Key']
            if key == f"{self._prefix}/": #ignore root
                continue
            yield key

    def get_keys(self):
        page_iterator = self.get_pages()
        for page in page_iterator:
            for key in self.get_keys_from_page(page):
                yield key

