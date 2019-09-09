def sort_by_two_keys(a, b):
    def _k(item):
        return item[a], item[b]

    return _k


def sort_by_int_key(a):
    def _k(item):
        return int(item[a])

    return _k