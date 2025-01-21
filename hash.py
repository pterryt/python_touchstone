import hashlib

# python's built-in hash function for md5
# we'll hash all the strings because there will be duplicates we don't want to store twice
# making ID from the tables no longer appropriate for storage
# this way when we return the strings to the JSONs in a future project lookups are faster
# even though it's not necessary for the test sample, it will be worth it once we're dealing with 100,000s,
# possibly even a million strings
def hash_string(value: str) -> str:

    return hashlib.md5(value.encode('utf-8')).hexdigest()