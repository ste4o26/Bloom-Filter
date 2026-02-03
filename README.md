# Bloom Filter

A space-efficient probabilistic data structure for fast membership testing with configurable false positive rates.

## Overview

This project implements a Bloom Filter, a data structure that determines whether an element is likely a member of a set or is sure that it is definitely not its member. It uses minimal memory while allowing for fast lookups, with a configurable trade-off between memory usage and false positive probability.

## Features

- **Multiple hash functions**: Support for MD5, SHA256, and MurmurHash3 as well as python's built in hash
- **Configurable accuracy**: Set desired false positive rates for your use case
- **Automatic sizing**: Calculates optimal bit array size and hash count based on data size and error tolerance
- **Serialization**: Can be configured to save and load filters to/from disk
- **Type-flexible**: Works with strings, numbers, bytes, dicts, lists, and tuples

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from bloom import BloomFilter

# Create a new filter expecting 1000 elements with 1% false positive rate
bf = BloomFilter.new(data_size=1000, false_positive_rate=0.01)

# Add elements
bf.add("apple")
bf.add("banana")
bf.add(42)

# Test membership
print("apple" in bf)    # True
print("orange" in bf)   # False (might return True with probability 0.01)
```

## Usage

### Creating a Filter

```python
# Automatic sizing based on expected data and false positive rate
bf = BloomFilter.new(data_size=1000, false_positive_rate=0.01)

# Manual creation with custom hash function
from utils import sha256
bf = BloomFilter(
    array=numpy.zeros(384, dtype=bool),
    hash_func=sha256,
    hashes_count=7
)
```

### Basic Operations

```python
bf.add(element)           # Add an element
element in bf             # Test membership
```

## Testing

Run the test suite:

```bash
python -m unittest tests.test_bloom
```

## Project Structure

- **bloom.py**: Core BloomFilter implementation
- **constants.py**: Type definitions and constants
- **utils.py**: Hash functions (MD5, SHA256) and utilities
- **hash_lib/murmurhash/**: Cython implementation of MurmurHash3
- **tests/**: Unit tests

## How It Works

A Bloom Filter uses:
1. A bit array initialized to all zeros
2. Multiple hash functions to map elements to array indices
3. For each added element, all hash functions set corresponding bits to 1
4. For membership testing, all hash bits must be 1 (possible false positives, no false negatives)

Memory usage grows logarithmically with data size, making it ideal for large datasets.
