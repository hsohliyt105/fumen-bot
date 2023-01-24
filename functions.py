# -*- coding: utf-8 -*-

from typing import Dict, List, Optional
from re import findall

from tinyurl_api import get_redirection

def get_fumen(string: str) -> Optional[str]:
    tinyurl = get_tinyurl(string)

    if tinyurl is not None:
        try:
            string += " " + get_redirection(tinyurl)

        except ValueError:
            pass
        
    found = findall('([vmd](110|115)@[\w+/?]+)', string)

    if len(found) > 0:
        return found[0][0]

    return None

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

def get_tinyurl(string: str) -> Optional[str]:
    found = findall('(https://(tinyurl\.com|tiny\.one|rotf\.lol)/[^ \n]*)', string)

    if len(found) > 0:
        return found[0][0]

    return None