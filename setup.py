#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='Police API',
    version='0.1',
    description='Python client library for the Police.uk API',
    author='Rock Kitchen Harris',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
