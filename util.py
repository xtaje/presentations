
def get_file(client, bucket_name, key):
        buf = io.BytesIO()
        client.download_fileobj(bucket_name, key, buf)

        # Decode and drop empty lines
        buf.seek(0)
        lines = (line.decode().strip() for line in buf.readlines())
        return list(filter(lambda x:x, lines))

