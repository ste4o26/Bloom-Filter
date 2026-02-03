from pathlib import Path

from Cython.Build import cythonize
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

PATH = Path(__file__).resolve().parent


class InplaceBuildExt(build_ext):
    """Subclass setuptools build extension class"""

    def build_extensions(self) -> None:
        """Overwrites where the output build should be placed."""
        self.build_lib = str(PATH)
        self.build_temp = str(PATH / "build")
        super().build_extensions()


def setup_package() -> None:
    """Set up the package bindings and generates a build"""
    setup(
        name="murmur",
        ext_modules=cythonize(
            [
                Extension(
                    "murmur",
                    sources=[str(PATH / "murmur.pyx"), str(PATH / "MurmurHash3.cpp")],
                    include_dirs=[str(PATH / "include")],
                    extra_compile_args=["-O3"],
                    language="c++",
                )
            ],
            language_level="3",
        ),
        package_data={"": ["*.pyx", "*.pxd", "include/murmurhash/*.h"]},
        cmdclass={"build_ext": InplaceBuildExt},
    )


if __name__ == "__main__":
    setup_package()
