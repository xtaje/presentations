def find_bad_articles(items, predicate):
    return filter(predicate, items)

def _find_bad_articles(items, predicate):
    for key, lines in items:
            if predicate(lines):
                yield key

