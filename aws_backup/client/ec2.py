# coding: utf-8
import boto3

from .base import BaseClient
from ..exceptions import OptionIsNotEnough


class Ec2Client(BaseClient):
    resource_service = 'ec2'
    delete_condition = {
        'image_max_number': 'lt',
        'image_expiration': 'lt',
    }

    def __init__(self, *args, **kwargs):
        super(Ec2Client, self).__init__(*args, **kwargs)

        if not (self.options.instance_id or self.options.instance_name or self.options.instance_tag):
            raise OptionIsNotEnough('At least one is required: --instance-id, --instance-name, --instance-tag')

    @property
    def instances(self):
        filters = [
            {'Name': 'tag:{}'.format(k), 'Values': ['{}'.format(v)]}
            for k, v in (kv.split('/') for kv in self.options.instance_tag or [])
        ]
        if self.options.instance_name:
            filters.append({'Name': 'tag:Name', 'Values': self.options.instance_name or []})
        return self.resource.instances.filter(
            InstanceIds=self.options.instance_id or [],
            Filters=filters
        )

    def create_image(self, instance):
        try:
            image = instance.create_image(
                Name=self.generate_code(instance.id),
                Description=self.options.image_description,
                NoReboot=not self.options.reboot,
                DryRun=self.options.dry_run
            )
            self.logger.debug('* instance.tags: %s', instance.tags)
            if instance.tags:
                image.create_tags(DryRun=self.options.dry_run, Tags=instance.tags)

            self.logger.info('* created image: %s (%s)', image.name, image.id)
            return image
        except boto3.exceptions.botocore.exceptions.ClientError as e:
            self.logger.error(e)

    def delete_image(self, image):
        name = image.name
        snapshot_ids = [s['Ebs']['SnapshotId'] for s in image.block_device_mappings]
        if self.options.keep_snapshot or not snapshot_ids:
            delete_snapshots = []
        else:
            delete_snapshots = self.resource.snapshots.filter(SnapshotIds=snapshot_ids)

        image.deregister(DryRun=self.options.dry_run)
        self.logger.info('* deleted image: %s (%s)', name, image.id)

        for snapshot in delete_snapshots:
            snapshot.delete(DryRun=self.options.dry_run)
            self.logger.info('  * deleted snapshot: %s', snapshot.id)

    def delete_images(self, instance):
        for index, image in enumerate(sorted(
            self.resource.images.filter(Filters=[{'Name': 'name', 'Values': [
                self.generate_query(instance.id)]}]),
            reverse=True, key=lambda i: i.creation_date
        ), start=1):
            self.logger.debug('* image.creation_date: %s', image.creation_date)
            cdate = self.parse_cdate(image.creation_date)
            if self.is_delete({'image_max_number': index, 'image_expiration': self.now - cdate}):
                try:
                    self.delete_image(image)
                except boto3.exceptions.botocore.exceptions.ClientError as e:
                    self.logger.error(e)
