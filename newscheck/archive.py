import io


class S3Archive(object):
    def __init__(self, bucket_name, prefix, client):
        self._client=client
        self._bucket_name = bucket_name
        self._prefix = prefix

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
        return list(filter(lambda x:x, lines))


    def keys_from(self, page):
        for item in page['Contents']:
            key = item['Key']
            if key == f"{self._prefix}/": #ignore root
                continue
            yield key
