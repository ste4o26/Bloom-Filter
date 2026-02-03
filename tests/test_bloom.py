from typing import Callable, cast
import unittest

import numpy

from bloom import BloomFilter, HashConfig
from constants import HashFunc
from lib import murmur_hash
from utils import md5, sha256


class BloomFilterTests(unittest.TestCase):

    def _get_bloom_filters(self) -> list[BloomFilter]:
        """Returns a pre-configured list of bloom filters"""
        return [
            BloomFilter.new(data_size=40, false_positive_rate=0.01),
            BloomFilter(
                array=numpy.zeros(384, dtype=bool), hash_func=md5, hashes_count=7
            ),
            BloomFilter(
                array=numpy.zeros(384, dtype=bool), hash_func=sha256, hashes_count=7
            ),
            BloomFilter(
                array=numpy.zeros(384, dtype=bool),
                hash_func=murmur_hash,
                hashes_count=7,
            ),
        ]

    def test_bloom_filter_textual_data(self) -> None:
        """Tests bloom filter with textual dataset"""
        data = [
            "apple",
            "banana",
            "cherry",
            "date",
            "elderberry",
            "fig",
            "grape",
            "honeydew",
            "kiwi",
            "lemon",
            "mango",
            "nectarine",
            "orange",
            "papaya",
            "quince",
            "raspberry",
            "strawberry",
            "tangerine",
            "ugli",
            "vanilla",
            "watermelon",
            "xigua",
            "yam",
            "zucchini",
            "avocado",
            "blackberry",
            "cantaloupe",
            "dragonfruit",
            "eggfruit",
            "feijoa",
            "guava",
            "hackberry",
            "imbe",
            "jackfruit",
            "kumquat",
            "lime",
            "mulberry",
            "nutmeg",
            "olive",
        ]

        for bloom in self._get_bloom_filters():
            for datum in data:
                bloom.add(datum)

            expected_possibly_in = [
                "apple",
                "banana",
                "olive",
                "lime",
                "grape",
                "jackfruit",
            ]
            for datum in expected_possibly_in:
                self.assertIn(datum, bloom)

            expected_not_in = ["coconut", "pear", "plum", "soursop"]
            for datum in expected_not_in:
                self.assertNotIn(datum, bloom)

    def test_bloom_filter_dict_data(self) -> None:
        """Tests bloom filter with textual dataset"""
        data = [
            {"name": "Name01", "age": 20},
            {"name": "Name02", "age": 21},
            {"name": "Name03", "age": 22},
            {"name": "Name04", "age": 23},
            {"name": "Name05", "age": 24},
            {"name": "Name06", "age": 25},
            {"name": "Name07", "age": 26},
            {"name": "Name08", "age": 27},
            {"name": "Name09", "age": 28},
            {"name": "Name10", "age": 29},
            {"name": "Name11", "age": 30},
            {"name": "Name12", "age": 31},
            {"name": "Name13", "age": 32},
            {"name": "Name14", "age": 33},
            {"name": "Name15", "age": 34},
            {"name": "Name16", "age": 35},
            {"name": "Name17", "age": 36},
            {"name": "Name18", "age": 37},
            {"name": "Name19", "age": 38},
            {"name": "Name20", "age": 39},
            {"name": "Name21", "age": 40},
            {"name": "Name22", "age": 41},
            {"name": "Name23", "age": 42},
            {"name": "Name24", "age": 43},
            {"name": "Name25", "age": 44},
            {"name": "Name26", "age": 45},
            {"name": "Name27", "age": 46},
            {"name": "Name28", "age": 47},
            {"name": "Name29", "age": 48},
            {"name": "Name30", "age": 49},
            {"name": "Name31", "age": 50},
            {"name": "Name32", "age": 51},
            {"name": "Name33", "age": 52},
            {"name": "Name34", "age": 53},
            {"name": "Name35", "age": 54},
            {"name": "Name36", "age": 55},
            {"name": "Name37", "age": 56},
            {"name": "Name38", "age": 57},
            {"name": "Name39", "age": 58},
            {"name": "Name40", "age": 59},
        ]

        for bloom in self._get_bloom_filters():
            for datum in data:
                bloom.add(datum)

            expected_possibly_in = [
                {"name": "Name01", "age": 20},
                {"name": "Name10", "age": 29},
                {"name": "Name40", "age": 59},
                {"name": "Name31", "age": 50},
                {"name": "Name15", "age": 34},
                {"name": "Name22", "age": 41},
            ]
            for datum in expected_possibly_in:
                self.assertIn(datum, bloom)

            expected_not_in = [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 45},
                {"name": "Name50", "age": 70},
                {"name": "Carol", "age": 50},
            ]
            for datum in expected_not_in:
                self.assertNotIn(datum, bloom)

    def test_bloom_filter_numeric_data(self) -> None:
        """Tests bloom filter with numeric dataset"""
        data = [
            10000000,
            10000005,
            10000010,
            10000015,
            10000020,
            20000000,
            20000010,
            20000020,
            20000030,
            20000040,
            30000000,
            30000050,
            30000100,
            30000150,
            30000200,
            40000000,
            40000100,
            40000200,
            40000300,
            40000400,
            1.5e5,
            1.50001e5,
            1.50002e5,
            1.50003e5,
            1.50004e5,
            2.75e6,
            2.7501e6,
            2.7502e6,
            2.7503e6,
            2.7504e6,
            3.123e7,
            3.1235e7,
            3.124e7,
            3.1245e7,
            3.125e7,
            4.888e5,
            4.8881e5,
            4.8882e5,
            4.8883e5,
            4.8884e5,
        ]

        for bloom in self._get_bloom_filters():
            for datum in data:
                bloom.add(datum)

            expected_possibly_in = [
                10000000,
                30000100,
                40000400,
                1.50003e5,
                2.7504e6,
            ]
            for datum in expected_possibly_in:
                self.assertIn(datum, bloom)

            expected_not_in = [50000000, 4.88825e5, 3.12499e7, 20050000, 9.99e9]
            for datum in expected_not_in:
                self.assertNotIn(datum, bloom)

    def test_hash_function_deserialization(self) -> None:
        """Tests hash functions deserialization"""
        with self.subTest("Defined hash function"):
            bloom = BloomFilter(array=numpy.ndarray(5), hash_func=md5)
            hash_func = bloom.hash_config.hash_func

            self.assertEqual(hash_func.__module__, md5.__module__)
            self.assertEqual(hash_func.__name__, md5.__name__)
            self.assertEqual(hash_func.__wrapped__, md5)  # type: ignore

        with self.subTest("Murmur hash function - c/cpp library"):
            bloom = BloomFilter(array=numpy.ndarray(5), hash_func=murmur_hash)
            hash_func = bloom.hash_config.hash_func

            self.assertEqual(hash_func.__module__, murmur_hash.__module__)
            self.assertEqual(hash_func.__name__, murmur_hash.__name__)
            self.assertEqual(hash_func.__wrapped__, murmur_hash)  # type: ignore

        with self.subTest("Anonymous(lambda) hash function"):
            bloom = BloomFilter(array=numpy.ndarray(5), hash_func=lambda v: hash(v))
            self.assertRaisesRegex(
                AttributeError,
                f"module '{__name__}' has no attribute '<lambda>'",
                cast(Callable[[HashConfig], HashFunc], HashConfig.hash_func.fget),
                bloom.hash_config,
            )

        with self.subTest("Defined and moved hash function"):

            def stub_hash(element: bytes) -> int:
                return hash(element)

            bloom = BloomFilter(array=numpy.ndarray(5), hash_func=stub_hash)
            del stub_hash

            self.assertRaisesRegex(
                AttributeError,
                f"module '{__name__}' has no attribute 'stub_hash'",
                cast(Callable[[HashConfig], HashFunc], HashConfig.hash_func.fget),
                bloom.hash_config,
            )


if __name__ == "__main__":
    unittest.main()
