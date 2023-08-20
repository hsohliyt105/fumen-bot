# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Literal, Optional

version = "0.1.5"

presence_time = 60

class FourDefault():
    auto: bool = True
    duration: float = 0.5
    transparency: bool = True
    background: Optional[str] = "default"
    theme: Literal["light", "dark"] = "dark"
    comment: bool = True

@dataclass
class FourSettings():
    auto: Optional[bool] = None
    duration: Optional[float] = None
    transparency: Optional[bool] = None
    background: Optional[str] = None
    theme: Optional[Literal["light", "dark"]] = None
    comment: Optional[bool] = None