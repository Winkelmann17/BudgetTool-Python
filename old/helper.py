import re

def IsNum(string):
    """Function that tells whether a supplied string
    is a number or not."""
    val = re.match(r"^(0|[1-9][0-9]*)$", string)
    return val