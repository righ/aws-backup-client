# coding: utf-8
import logging
from datetime import datetime

import boto3

AWS_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class BaseClient(object):
    resource_service = None
    client_service = None

    def __init__(self, logger, options):
        logger.setLevel(options.log_level)
        logger.addHandler(logging.StreamHandler())
        self.logger = logger
        self.options = options
        if self.resource_service:
            self.resource = boto3.resource(
                self.resource_service,
                aws_access_key_id=options.aws_access_key_id,
                aws_secret_access_key=options.aws_secret_access_key,
                region_name=options.aws_region
            )

        if self.client_service:
            self.client = boto3.client(
                self.client_service,
                aws_access_key_id=options.aws_access_key_id,
                aws_secret_access_key=options.aws_secret_access_key,
                region_name=options.aws_region
            )

        if self.options.preload:
            self.preloaded = __import__(self.options.preload)

        logger.debug('* options: %s', options)

    @property
    def now(self):
        if self.options.client_time_diff:
            return datetime.now() + self.options.client_time_diff
        return datetime.now()

    def parse_cdate(self, cdate):
        cdate = datetime.strptime(cdate, AWS_TIME_FORMAT)
        if self.options.aws_time_diff:
            return cdate + self.options.aws_time_diff
        return cdate

    def generate_query(self, id):
        return '{prefix}{id}-*'.format(prefix=self.options.prefix, id=id)

    def generate_code(self, id):
        return '{prefix}{id}-{time}'.format(
            prefix=self.options.prefix, id=id,
            time=self.now.strftime(self.options.client_time_format)
        )

    def extract_name(self, tags):
        return {
            t['Key']: t['Value']
            for t in tags or []}.get('Name', 'noname')
