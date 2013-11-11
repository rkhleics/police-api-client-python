#!/usr/bin/env python

from setuptools import setup, find_packages

import police_api

setup(
    name='police-api-client',
    version=police_api.__version__,
    description='Python client library for the Police API',
    author='Rock Kitchen Harris',
    packages=find_packages(),
    install_requires=[
        'requests==2.0.0',
    ],
)
