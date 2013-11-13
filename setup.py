#!/usr/bin/env python

from setuptools import setup, find_packages

execfile('police_api/version.py')

setup(
    name='police-api-client',
    version=__version__,  # NOQA
    description='Python client library for the Police API',
    long_description=open('README.rst').read(),
    author='Rock Kitchen Harris',
    license='MIT',
    url='https://github.com/rkhleics/police-api-client-python',
    download_url='https://github.com/rkhleics/police-api-client-python/downloads',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests==2.0.0',
    ],
)
