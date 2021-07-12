from typing import Union, List


def is_float(text: str) -> bool:
    try:
        float(text)
        return True
    except:
        return False


def is_int(text: str) -> bool:
    try:
        int(text)
        return True
    except:
        return False

