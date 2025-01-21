import re

def contains_hanzi(string:str) -> bool:
    pattern = re.compile(r"[\u4e00-\u9fff]")
    return bool(pattern.search(string))