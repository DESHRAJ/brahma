from collections import defaultdict
from aws.sgs import get_all_sgs
from aws.ec2 import get_all_running_instances


def get_sg_info_for_port(port=22):
    sgs = get_all_sgs()
    all_instances = get_all_running_instances()

    sg_instances_map = defaultdict(list)

    for instance in all_instances:
        sec_groups = instance.security_groups
        for sg in sec_groups:
            group_id = sg.get('GroupId')
            sg_instances_map[group_id].append(instance)

    for group_id, instances in sg_instances_map.iteritems():
        print group_id, sgs.get(group_id).description
        print "="*40

        for instance in instances:
            row = "{ip_address} {key_name}".format(ip_address=instance.public_ip_address,
                    key_name=instance.key_name)
            print row
