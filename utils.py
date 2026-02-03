import functools
import hashlib
import importlib
import json
from typing import cast

from constants import ENCODING, ElementType, HashFunc


def import_hash_function(import_path: str) -> HashFunc:
    """Imports a hash function for any given import path"""
    module_name, func_name = import_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    member = getattr(module, func_name)
    if not callable(member):
        raise RuntimeError(f"Member {member.__name__} is not a function!")
    return cast(HashFunc, member)


def seed_hash(hash_func: HashFunc) -> HashFunc:
    """Wraps any hash function to accept a seed argument"""

    @functools.wraps(hash_func)
    def wrap(element: ElementType, *args, seed: int = 0, **kwargs) -> int:
        """Hash function wrapper"""
        if not isinstance(element, bytes):
            element = json.dumps(element, sort_keys=True).encode(ENCODING)
        seed_bytes = seed.to_bytes(8, "big", signed=False)
        return hash_func(seed_bytes + element, *args, **kwargs)

    return wrap


def md5(element: bytes) -> int:
    """Hashlib md5 cryptographic hash function wrapper"""
    return int(hashlib.md5(element).hexdigest(), 16)


def sha256(element: bytes) -> int:
    """Hashlib sha256 cryptographic hash function wrapper"""
    return int(hashlib.sha256(element).hexdigest(), 16)
