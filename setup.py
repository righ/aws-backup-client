#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

__author__ = 'righ'
__author_email__ = 'righ.m9@gmail.com'
__version__ = '0.0.3'
__license__ = 'Apache License 2.0'

__name__ = 'aws-backup-client'
__url__ = 'https://github.com/righ/' + __name__

__short_description__ = 'aws backup clients'
__long_description__ = open('./README.rst', 'r').read()

__classifiers__ = [
    'Environment :: Console',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Topic :: Software Development',
]
__keywords__ = [
    'aws',
    'backup',
    'ec2',
    'ami',
]

__install_requires__ = [
    'boto3',
]

__entry_points__ = {
    'console_scripts': [
        'ec2ami-backup = aws_backup.bin.ec2:ami'
    ],
}

setup(
    name=__name__,
    version=__version__,
    description=__short_description__,
    long_description=__long_description__,
    classifiers=__classifiers__,
    keywords=', '.join(__keywords__),
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    install_requiers=__install_requires__,
    packages=find_packages(exclude=['*.tests.*']),
    entry_points=__entry_points__,
)
