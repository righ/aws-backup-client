# coding: utf-8
import re
import logging
import argparse
from functools import reduce

from .compat import timedelta


class TypeDelta(object):
    def __init__(self, cls=timedelta):
        self.cls = cls

    def __call__(self, deltastr=''):
        return reduce(self.cls.__add__, (
            self.parse(token) for token in deltastr.split()))

    def parse(self, token):
        match = re.search(r'[0-9+\-]+', token)
        return self.cls(**{
            token[match.end():] or 'days': int(match.group())
        })


parser = argparse.ArgumentParser()
parser.add_argument("--aws-access-key-id", help="aws access key id")
parser.add_argument("--aws-secret-access-key", help="aws secret access key")
parser.add_argument("--aws-region", help="aws region")
parser.add_argument("--aws-timedelta", type=TypeDelta(), help="time difference of aws host")
parser.add_argument("--client-timedelta", type=TypeDelta(), help="time difference of client host")
parser.add_argument("--client-timefmt", help="time format as part of name", default='%Y-%m-%dT%H-%M')
parser.add_argument("--log-level", type=int, help="log level", default=logging.INFO)
parser.add_argument("--reboot", help="reboot", action="store_true")
parser.add_argument("--dry-run", help="dry run", action="store_true")
parser.add_argument("--prefix", help="backup name of prefix", default='')
