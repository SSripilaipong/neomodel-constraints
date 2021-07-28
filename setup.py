import setuptools
from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

NAME = 'neomodel_constraints'
VERSION = '0.0.1'
URL = 'https://github.com/SSripilaipong/neomodel_constraints'
LICENSE = 'MIT'
AUTHOR = 'SSripilaipong'
EMAIL = 'SHSnail@mail.com'


setup(
    name=NAME,
    version=VERSION,
    packages=setuptools.find_packages(),
    url=URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=None,
    long_description=None,
    python_requires='>=3.6',
    install_requires=requirements,
    classifiers=None,
)
