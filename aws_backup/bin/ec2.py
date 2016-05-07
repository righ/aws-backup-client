#!/usr/bin/env python
# coding: utf-8
import logging

from ..parser import parser, TypeDelta
from ..client.ec2 import Ec2Client


def ami(*args):
    logger = logging.getLogger('aws-backup-client.ami')

    for arg in args:
        parser.add_argument(arg)

    parser.add_argument("--instance-id", help="instance id", action='append')
    parser.add_argument("--instance-name", help="instance name, '*' can be used as wildcard.", action='append')
    parser.add_argument("--instance-tag", help="instance tag in the form of 'name/value', '*' can be used as wildcard in part of tag value.", action='append')

    parser.add_argument("--image-description", help="image description", default='')
    parser.add_argument("--image-max-number", type=int, help="image max number", default=None)
    parser.add_argument("--image-expiration", type=TypeDelta(), help="image expiration", default=None)

    ec2 = Ec2Client(logger, options=parser.parse_args())
    for instance in ec2.instances:
        logger.info('[%s (%s)]', ec2.extract_name(instance.tags), instance.id)
        ec2.create_image(instance)
        ec2.delete_images(instance)
