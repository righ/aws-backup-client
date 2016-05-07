# coding: utf-8
import logging
from datetime import datetime, timedelta
from unittest import TestCase

from .compat import mock


class TestEc2Client(TestCase):
    def _callFUT(self, *args, **kwargs):
        from ..bin.ec2 import ami
        return ami(*args, **kwargs)

    @mock.patch('aws_backup.bin.ec2.Ec2Client')
    def test_ami(self, DummyEc2Client):
        ec2 = DummyEc2Client()
        ec2.instances = [1, 2]
        self._callFUT()
        self.assertEqual(ec2.create_image.call_count, 2)
        self.assertEqual(ec2.delete_images.call_count, 2)
