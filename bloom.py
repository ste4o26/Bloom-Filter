from dataclasses import dataclass
import json
import math
from typing import Iterator, Self

import numpy

from constants import (
    BASE_SEED_1,
    BASE_SEED_2,
    ENCODING,
    ElementType,
    HashFunc,
    MAX_FALSE_POSITIVE,
)
from utils import import_hash_function, seed_hash


@dataclass(frozen=True)
class HashConfig:
    """Represents hash function configuration"""

    hash_function_import_path: str
    hashes_count: int = 1

    @property
    def hash_func(self) -> HashFunc:
        """Deserializes the hash function"""
        hash_func = import_hash_function(self.hash_function_import_path)
        return seed_hash(hash_func)


@dataclass(frozen=True)
class BloomFilter:
    """Space-efficient probabilistic data structure"""

    array: numpy.ndarray
    hash_config: HashConfig
    path: str = ""

    def __init__(
        self,
        array: numpy.ndarray,
        hash_func: HashFunc | None = None,
        hashes_count: int = 1,
    ) -> None:
        """Initialize new BloomFilter"""
        hash_func = hash_func or hash
        hash_config = HashConfig(
            f"{hash_func.__module__}.{hash_func.__name__}", hashes_count or 1
        )
        object.__setattr__(self, "array", array)
        object.__setattr__(self, "hash_config", hash_config)

    @classmethod
    def new(
        cls, *, data_size: int, false_positive_rate: float = MAX_FALSE_POSITIVE
    ) -> Self:
        """
        Instantiate the filter

        Parameters
        ----------
        data_size: Length of the elements you will insert to the filter (n)
        false_positive_rate: The number of false positives that are tolerated (p)
            Where k * 100 gives the percentage
        """
        array_size = cls.calculate_bit_array_size(
            data_size=data_size, false_positive_rate=false_positive_rate
        )
        array = numpy.zeros(array_size, dtype=bool)
        hashes_count = cls.calculate_hashes_count(
            array_size=array_size, data_size=data_size
        )
        return cls(array=array, hashes_count=hashes_count)

    @staticmethod
    def calculate_bit_array_size(*, data_size: int, false_positive_rate: float) -> int:
        """
        Calculates the number of bits needed
        for a given size and false positive rate
        """
        num_bits = -(data_size * math.log(false_positive_rate)) / (math.log(2) ** 2)
        return math.ceil(num_bits)

    @staticmethod
    def calculate_hashes_count(*, array_size: int, data_size: int) -> int:
        """
        Calculates the number of hash functions needed
        for a given number of bits and size
        """
        num_hashes = (array_size / data_size) * math.log(2)
        return math.ceil(num_hashes)

    def add(self, element: ElementType) -> None:
        """Adds a new element to the filter"""
        for seed in range(self.hash_config.hashes_count):
            index = self._hash(element, seed) % len(self.array)
            self.array[index] = True

    def validate(self) -> None:
        """Validates the filter before saving it"""
        class_name = self.__class__.__name__
        if not self.path.strip():
            raise ValueError(f"{class_name} path field is required!")
        if len(self.array) == 0:
            raise ValueError(
                f"{class_name} bit array should not be empty!",
            )
        if not self.hash_config.hash_function_import_path:
            raise ValueError(
                f"{class_name} hash function is required!",
            )

    def _hash(self, element: ElementType, seed: int) -> int:
        """Double hashes the input for better distribution"""
        if not isinstance(element, bytes):
            element = json.dumps(element, sort_keys=True).encode(ENCODING)
        h1 = self.hash_config.hash_func(element, seed=BASE_SEED_1)
        h2 = self.hash_config.hash_func(element, seed=BASE_SEED_2)
        return (h1 + seed * h2) & ((1 << 64) - 1)

    def __iter__(self) -> Iterator[bool]:
        """Implements iter for the filter"""
        return iter(self.array)

    def __contains__(self, element: ElementType) -> bool:
        """Whether and element is possibly in the filter"""
        for seed in range(self.hash_config.hashes_count):
            index = self._hash(element, seed) % len(self.array)
            if not self.array[index]:
                return False
        return True
