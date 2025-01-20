import hashlib

def hash_string(value: str) -> str:

    return hashlib.md5(value.encode('utf-8')).hexdigest()