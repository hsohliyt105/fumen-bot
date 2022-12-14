# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Tuple
from re import findall

def get_fumen(strings: List[str]) -> str:
    for string in strings:
        found = findall('([vmd](110|115)@[\w+/?]+)', string)

        if len(found) > 0:
            return found[0][0]

    return None

def get_options(strings: List[str]) -> Dict:
    result = {}

    for string in strings:
        found = findall('(.+)=(.+)', string)

        if len(found) > 0:
            result[found[0][0].lower()] = found[0][1].lower()

    return result

def is_colour_code(string: str) -> bool:
    if string[0] != "#" or len(string) != 7:
        return False

    try:
        red = int(string[1:2], 16)
        green = int(string[3:4], 16)
        blue = int(string[5:6], 16)

        return True if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255 else False

    except:
       return False

def get_tinyurl(strings: List[str]) -> Optional[Tuple[str]]:
    for string in strings:
        found = findall('(https://(tinyurl\.com|tiny\.one|rotf\.lol)/[^ \n]*)', string)

        if len(found) > 0:
            return found[0][0]

    return None