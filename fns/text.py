import hashlib


def md5_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def window(tokens, size=3):
    return [(tokens[i: i + size], tokens[i + size])
            for i in range(0, len(tokens) - size, 1)]
