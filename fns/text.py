import hashlib

def md5_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()
