def find_bad_articles(items, predicate):
    found = filter(predicate, items)
    return map(lambda item: item[0], found)

def _find_bad_articles(items, predicate):
    for key, lines in items:
        if predicate(lines):
            yield key

