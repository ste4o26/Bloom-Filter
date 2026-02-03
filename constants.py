from typing import Callable


MAX_FALSE_POSITIVE = 1e-7
"""Max false positive tolerance"""

ENCODING = "utf-8"
"""Encoding format"""

BASE_SEED_1 = 0x9E3779B97F4A7C15
"""Low corelation golden ratio 64 bit hashing constant"""

BASE_SEED_2 = 0xD1B54A32D192ED03
"""Another good 64 bit hashing constant independent of the golden ratio one"""

type ElementType = tuple | list | dict | str | int | float | bytes
"""Possible element types accepted by the bloom filter"""

type HashFunc = Callable[..., int]
"""Hash function type definition accepted by the boom filter"""
