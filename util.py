
def get_file(client, bucket_name, key):
        buf = io.BytesIO()
        client.download_fileobj(bucket_name, key, buf)

        # Decode and drop empty lines
        buf.seek(0)
        lines = (line.decode().strip() for line in buf.readlines())
        return list(filter(lambda x:x, lines))

def check_article(lines, threshold, stock_symbols):
    limit = threshold * len(lines)
    while lines and limit:
        line = lines.pop()
        first_word = line.split()[0]
        if first_word in stock_symbols:
            limit -= 1

    return limit <= 0

def get_pages(client, bucket_name, prefix):
    paginator = client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    return page_iterator
