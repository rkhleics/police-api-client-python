#!/usr/bin/env python

from setuptools import setup, find_packages

execfile('police_api/version.py')

setup(
    name='police-api-client',
    version=__version__,  # NOQA
    description='Python client library for the Police API',
    author='Rock Kitchen Harris',
    packages=find_packages(),
    install_requires=[
        'requests==2.0.0',
    ],
)
