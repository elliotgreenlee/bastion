import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "Bastion",
    version = "0.1.0",
    author = "Elliot Greenlee and Jared M. Smith",
    author_email = "jms@vols.utk.edu",
    description = ("CS560 Programming Assignment 1"),
    license = "MIT",
    keywords = "filesystem shell",
    url = "https://lambentlight.github.io/bastion/",
    packages=['bastion', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
