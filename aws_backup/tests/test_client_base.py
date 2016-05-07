# coding: utf-8
import logging
from datetime import datetime
from unittest import TestCase

from .compat import mock


class TestBaseClient(TestCase):
    def _makeOne(self, *args, **kwargs):
        from ..client.base import BaseClient
        return BaseClient(logging.getLogger(), self._makeOption(args))

    def _makeOption(self, args):
        from ..parser import parser
        return parser.parse_args(args)

    def test_preload(self):
        cli = self._makeOne('--preload', 'sys')
        import sys
        self.assertEqual(cli.preloaded, sys)

    @mock.patch('aws_backup.client.base.datetime')
    def test_now(self, dummy_datetime):
        dummy_datetime.now.return_value = datetime(1988, 5, 22)
        cli = self._makeOne()
        self.assertEqual(cli.now, datetime(1988, 5, 22))

        cli = self._makeOne('--client-time-diff', '9hours')
        self.assertEqual(cli.now, datetime(1988, 5, 22, 9))

    def test_parse_cdate(self):
        cli = self._makeOne('--aws-time-diff', '9hours')
        self.assertEqual(
            cli.parse_cdate('1988-05-22T00:30:00.000Z'),
            datetime(1988, 5, 22, 9, 30))

    def test_generate_query(self):
        cli = self._makeOne('--prefix', 'monthly-')
        self.assertEqual(
            cli.generate_query('test'),
            'monthly-test-*')

    @mock.patch('aws_backup.client.base.datetime')
    def test_generate_code(self, dummy_datetime):
        dummy_datetime.now.return_value = datetime(1988, 5, 22)
        cli = self._makeOne(
            '--prefix', 'monthly-',
            '--client-time-format', '%Y%m')
        self.assertEqual(
            cli.generate_code('test'),
            'monthly-test-198805')

    def test_extract_name(self):
        cli = self._makeOne()
        self.assertEqual(
            cli.extract_name([
                {'Key': 'Name', 'Value': 'testname'},
                {'Key': 'Name2', 'Value': 'testaaa'},
            ]), 'testname')

        self.assertEqual(cli.extract_name([]), 'noname')
