from setuptools import setup
from warnings import warn
import sys

if sys.version_info.major < 3:
    warn("This implementation was made for Python 3, so it might not work with Python 2")

setup(
    name="xTraktor",
    version="0.1",
    description="Data extractor and serializer for the world wide web.",
    author="Andraz Povse, Matej Klemen, Jaka Stavanja",
    packages=["implementation"]
)
