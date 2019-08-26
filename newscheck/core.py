from newscheck import config
from newscheck import stock 
from newscheck.archive import S3Archive

def find_bad_articles(bucket_name, predicate):
    archive = S3Archive(bucket_name, config.PREFIX, config.REGION_NAME)
    for page in archive.get_pages():
        for key in archive.keys_from(page):
            lines = archive.get_file(key)
            if predicate(lines):
                yield key

