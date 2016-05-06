# coding: utf-8
import sys
import logging
from datetime import datetime

import boto3

AWS_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class BaseClient(object):
    service = None

    def __init__(self, logger, options):
        logger.setLevel(options.log_level)
        logger.addHandler(logging.StreamHandler())
        self.logger = logger
        self.options = options
        self.resource = boto3.resource(
            self.service,
            aws_access_key_id=options.aws_access_key_id,
            aws_secret_access_key=options.aws_secret_access_key,
            region_name=options.aws_region
        )
        logger.debug('options: %s', options)

    @property
    def now(self):
        if self.options.client_timedelta:
            return datetime.now() + self.options.client_timedelta
        return datetime.now()

    def parse_cdate(self, cdate):
        cdate = datetime.strptime(cdate, AWS_TIME_FORMAT)
        if self.options.aws_timedelta:
            return cdate + self.options.aws_timedelta
        return cdate

    def generate_query(self, obj):
        return '{prefix}{id}-*'.format(prefix=self.options.prefix, id=obj.id)

    def generate_code(self, obj):
        return '{prefix}{id}-{time}'.format(
            prefix=self.options.prefix, id=obj.id,
            time=self.now.strftime(self.options.client_timefmt)
        )

    def extract_name(self, tags):
        return {
            t['Key']: t['Value']
            for t in tags or []}.get('Name', 'noname')
