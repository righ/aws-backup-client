# coding: utf-8
import boto3

from .base import BaseClient
from ..compat import timedelta


class Ec2Client(BaseClient):
    service = 'ec2'

    @property
    def instances(self):
        return self.resource.instances.filter(
            InstanceIds=self.options.instance)

    def create_image(self, instance):
        try:
            image = instance.create_image(
                Name=self.generate_code(instance),
                Description=self.options.image_description,
                NoReboot=not(self.options.reboot),
                DryRun=self.options.dry_run
            )
            self.logger.debug('instance.tags: %s', instance.tags)
            image.create_tags(DryRun=self.options.dry_run, Tags=[{
                'Key': 'Name',
                'Value': self.extract_name(instance.tags),
            }])

            self.logger.info(
                'created image: %s (%s)', image.name, image.id)
            return image
        except boto3.exceptions.botocore.exceptions.ClientError as e:
            self.logger.error(e)

    def delete_images(self, instance):
        if not (self.options.image_max_number or self.options.image_expiration):
            return

        for index, image in enumerate(sorted(
            self.resource.images.filter(Filters=[{'Name': 'name', 'Values': [
                self.generate_query(instance)]}]),
            reverse=True, key=lambda i: i.creation_date
        ), start=1):
            self.logger.debug('image.creation_date: %s', image.creation_date)
            cdate = self.parse_cdate(image.creation_date)
            if (
                (not self.options.image_max_number or index > self.options.image_max_number) and
                (not self.options.image_expiration or cdate + self.options.image_expiration < self.now)
            ):
                try:
                    name = image.name
                    image.deregister(DryRun=self.options.dry_run)
                    self.logger.info(
                        'deleted image: %s (%s)', name, image.id)
                except boto3.exceptions.botocore.exceptions.ClientError as e:
                    self.logger.error(e)
