"""Amazon EC2 related utility functions.
"""

import boto3


def get_all_running_instances():
    ec2 = boto3.resource('ec2')
    instances = list(ec2.instances.filter())
    return instances
