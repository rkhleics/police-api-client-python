#!/usr/bin/env python

from setuptools import setup, find_packages

from police_api.version import __version__

setup(
    name='police-api-client',
    version=__version__,
    description='Python client library for the Police API',
    author='Rock Kitchen Harris',
    packages=find_packages(),
    install_requires=[
        'requests==2.0.0',
    ],
)
