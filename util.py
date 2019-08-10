
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
