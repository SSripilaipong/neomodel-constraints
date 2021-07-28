import setuptools
from setuptools import setup


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

NAME = 'neomodel-constraints'
VERSION = '0.0.2'
URL = 'https://github.com/SSripilaipong/neomodel-constraints'
LICENSE = 'MIT'
AUTHOR = 'SSripilaipong'
EMAIL = 'SHSnail@mail.com'
CONSOLE_SCRIPT = 'nmcon=neomodel_constraints.cli:main'

setup(
    name=NAME,
    version=VERSION,
    packages=['neomodel_constraints'],
    url=URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=None,
    long_description=None,
    python_requires='>=3.6',
    install_requires=requirements,
    classifiers=[],
    entry_points={
        'console_scripts': [CONSOLE_SCRIPT],
    }
)
