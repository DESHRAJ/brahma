"""Amazon EC2 Security Groups related utilities.
"""

import boto3

from django.conf import settings



def get_all_sgs():
    """Returns all Security groups in the default region as
    a mapping between security group id vs boto SecurityGroup object.
    """
    ec2 = boto3.resource('ec2')
    security_groups = list(ec2.security_groups.all())
    return security_groups
