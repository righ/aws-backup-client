# coding: utf-8
import logging
from datetime import datetime, timedelta
from unittest import TestCase

from .compat import mock


class TestEc2Client(TestCase):
    def _makeOne(self, **options):
        from ..client.ec2 import Ec2Client
        return Ec2Client(logging.getLogger(), mock.MagicMock(**options))

    @mock.patch('aws_backup.client.base.boto3')
    def test_instances(self, dummy_boto):
        cli = self._makeOne(
            log_level=10,
            aws_access_key_id='testid',
            aws_secret_access_key='testkey',
            aws_region='testregion',
            instance_id=['id1', 'id2'],
            instance_name=['name1', 'name2', 'name3'],
            instance_tag=['k1/v1', 'k2/v2'],
            preload=None,
        )
        cli.instances
        dummy_boto.resource.assert_called_with(
            'ec2',
            aws_access_key_id='testid',
            aws_secret_access_key='testkey',
            region_name='testregion',
        )
        dummy_boto.resource().instances.filter.assert_called_with(
            InstanceIds=['id1', 'id2'],
            Filters=[
                {'Name': 'tag:k1', 'Values': ['v1']},
                {'Name': 'tag:k2', 'Values': ['v2']},
                {'Name': 'tag:Name', 'Values': ['name1', 'name2', 'name3']},
            ]
        )

    @mock.patch('aws_backup.client.base.datetime')
    @mock.patch('aws_backup.client.base.boto3')
    def test_create_image(self, dummy_boto, dummy_datetime):
        dummy_datetime.now.return_value = datetime(1988, 5, 22)
        cli = self._makeOne(
            log_level=10,
            instance_id=['id1', 'id2'],
            instance_name=['name1', 'name2', 'name3'],
            instance_tag=['k1/v1', 'k2/v2'],
            image_description='test description',
            reboot=True,
            dry_run=True,
            prefix='daily-',
            client_time_format='%Y%m%d',
            client_time_diff=None,
            preload=None,
        )
        instance = mock.MagicMock(
            tags=[{'Key': 'Name', 'Value': 'testname'}], id='testid')
        cli.create_image(instance)
        instance.create_image.assert_called_with(
            Name='daily-testid-19880522',
            Description='test description',
            NoReboot=False,
            DryRun=True,
        )
        instance.create_image().create_tags.assert_called_with(
            Tags=[{'Key': 'Name', 'Value': 'testname'}],
            DryRun=True
        )

    @mock.patch('aws_backup.client.base.datetime')
    @mock.patch('aws_backup.client.base.boto3')
    def test_delete_image_exceeded_number(self, dummy_boto, dummy_datetime):
        dummy_datetime.now.return_value = datetime(1988, 5, 22)
        cli = self._makeOne(
            log_level=30,
            dry_run=True,
            prefix='daily-',
            client_time_format='%Y%m%d',
            client_time_diff=None,
            image_max_number=2,
            image_expiration=None,
            preload=None,
        )
        images = [
            mock.MagicMock(
                name='image{}'.format(i),
                creation_date='2000-01-0{}T00:00:00.000Z'.format(i))
            for i in range(1, 6)]
        cli.resource.images.filter.return_value = images
        instance = mock.MagicMock(id='testid')
        cli.delete_images(instance)
        images[0].deregister.assert_called_with(DryRun=True)
        images[1].deregister.assert_called_with(DryRun=True)
        images[2].deregister.assert_called_with(DryRun=True)
        self.assertFalse(images[3].deregister.called)
        self.assertFalse(images[4].deregister.called)

    @mock.patch('aws_backup.client.base.datetime')
    @mock.patch('aws_backup.client.base.boto3')
    def test_delete_image_exceeded_expiration(self, dummy_boto, dummy_datetime):
        dummy_datetime.now.return_value = datetime(2000, 1, 6)
        dummy_datetime.strptime = datetime.strptime
        cli = self._makeOne(
            aws_time_diff=None,
            log_level=30,
            dry_run=True,
            prefix='daily-',
            client_time_format='%Y%m%d',
            client_time_diff=None,
            image_max_number=None,
            image_expiration=timedelta(days=3),
            instace_name='*',
            preload=None,
        )
        images = [
            mock.MagicMock(
                name='image{}'.format(i),
                creation_date='2000-01-0{}T00:00:00.000Z'.format(i))
            for i in range(1, 6)]
        cli.resource.images.filter.return_value = images
        instance = mock.MagicMock(id='testid')
        cli.delete_images(instance)
        images[0].deregister.assert_called_with(DryRun=True)  # 1 + 3 < 6
        images[1].deregister.assert_called_with(DryRun=True)  # 2 + 3 < 6
        self.assertFalse(images[2].deregister.called)  # 3 + 3 = 6
        self.assertFalse(images[3].deregister.called)  # 4 + 3 > 6
        self.assertFalse(images[4].deregister.called)  # 5 + 3 > 6

    @mock.patch('aws_backup.client.base.boto3')
    def test_raise_option_does_not_enough(self, dummy_boto):
        from ..exceptions import OptionIsNotEnough
        with self.assertRaises(OptionIsNotEnough):
            self._makeOne(
                log_level=30,
                preload=None,
                instance_id=None,
                instance_name=None,
                instance_tag=None,
            )

    @mock.patch('aws_backup.client.base.datetime')
    @mock.patch('aws_backup.client.base.boto3')
    def test_delete_snapshot(self, dummy_boto, dummy_datetime):
        dummy_datetime.now.return_value = datetime(1988, 5, 22)
        cli = self._makeOne(
            log_level=30,
            dry_run=True,
            prefix='daily-',
            client_time_format='%Y%m%d',
            client_time_diff=None,
            image_max_number=1,
            image_expiration=None,
            preload=None,
            keep_snapshot=False
        )
        images = [
            mock.MagicMock(
                name='image{}'.format(i),
                creation_date='2000-01-0{}T00:00:00.000Z'.format(i),
                block_device_mappings=[{'Ebs': {'SnapshotId': 'test'}}],
            )
            for i in range(1, 4)]

        m = mock.MagicMock()
        m2 = mock.MagicMock()
        delete_snapshots = [m, m2]

        cli.resource.images.filter.return_value = images
        cli.resource.snapshots.filter.return_value = delete_snapshots
        instance = mock.MagicMock(id='testid')
        cli.delete_images(instance)
        self.assertEqual(m.delete.call_count, 2)
        self.assertEqual(m2.delete.call_count, 2)
