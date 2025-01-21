import re

# check a string for any Unicode characters falling in the values between u4e00 and u9ffff
# these are where Chinese characters are mapped, and it will tell us if we are dealing with a string
# that has Chinese in it
def contains_hanzi(string:str) -> bool:
    pattern = re.compile(r"[\u4e00-\u9fff]")
    return bool(pattern.search(string))