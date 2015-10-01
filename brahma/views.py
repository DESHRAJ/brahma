from collections import namedtuple
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from aws.sgs import get_all_sgs

import json


SG = namedtuple('SecurityGroup', 'group_name group_id vpc_id sources')

def index(request):
    template = 'base.html'
    return render_to_response(template, {})

@csrf_exempt
def manage_security_groups_ssh(request):
    all_sec_groups = get_all_sgs() 

    ssh_ports_info = get_port_info(all_sec_groups, port=22)
    html = render_to_string('ssh_ports.html', {'sec_groups': ssh_ports_info})

    response = {
        'response': html,
        'status': 'OK'
    }

    resp = json.dumps(response)
    return HttpResponse(resp)

def get_port_info(all_security_groups, port=22):
    info = []

    for sgroup in all_security_groups:
        group_name = sgroup.group_name
        group_id = sgroup.id
        vpc_id = sgroup.vpc_id or ''

        sources = []
        ip_permissions = sgroup.ip_permissions
        
        for ip_perm in ip_permissions:
            from_port = ip_perm.get('FromPort')
            to_port = ip_perm.get('ToPort')

            if from_port<= port and port<= to_port:
                ip_ranges = ip_perm.get('IpRanges')
                if ip_ranges:
                    sources.append(ip_ranges[0].get('CidrIp'))
                else:
                    groups = ip_perm.get('UserIdGroupPairs')
                    if groups:
                        group_names = [gp.get('GroupName') for gp in groups]
                        group_names = [gn for gn in group_names if gn]

                        print group_names
                        if group_names:
                            sources = group_names
                    else:
                        print ip_perm

        sg = SG(group_name=group_name, vpc_id=vpc_id, sources=sources,
                group_id=group_id)
        info.append(sg)
    info.sort(key=(lambda x: x.group_name))
    return info
