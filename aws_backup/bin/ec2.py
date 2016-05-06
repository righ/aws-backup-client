#!/usr/bin/env python
# coding: utf-8
import sys
import logging

from ..parser import parser, TypeDelta
from ..client.ec2 import Ec2Client


def ami():
    logger = logging.getLogger('ec2ami')

    parser.add_argument("--instance", help="instance id", action='append', required=True)
    parser.add_argument("--image-description", help="image description", default='')
    parser.add_argument("--image-max-number", type=int, help="image max number", default=None)
    parser.add_argument("--image-expiration", type=TypeDelta(), help="image expiration", default=None)

    ec2 = Ec2Client(logger, options=parser.parse_args())
    for instance in ec2.instances:
        ec2.create_image(instance)
        ec2.delete_images(instance)
