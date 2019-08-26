def find_bad_articles(archive, predicate):
    for page in archive.get_pages():
        for key in archive.keys_from(page):
            lines = archive.get_file(key)
            if predicate(lines):
                yield key

