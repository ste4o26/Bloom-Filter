## Licenses and Credits

This project is licensed under the MIT License.
See the [LICENSE](./LICENSE) file for details.

Portions of this software are derived from the
[murmurhash](https://github.com/explosion/murmurhash) library
by Explosion AI, specifically the MurmurHash3 implementation.
Used under the terms of the MIT License.
See [LICENSE](./LICENSE) for details.

### About MurmurHash3

MurmurHash3 is a high-quality, non-cryptographic hash function
designed for speed and uniform distribution. It’s widely used
in systems such as data processing pipelines, hash tables,
and feature hashing for machine learning.


## Building from Source

If you want to (re)build the Cython/C++ extension for murmurhas,
you can use the `setup.py` build command.

python3 <path_to_murmurhash>/setup.py build_ext --inplace --verbose
