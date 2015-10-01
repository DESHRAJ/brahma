from django.shortcuts import render_to_response

from aws.sgs import get_all_sgs


def index(request):
    template = 'base.html'
    return render_to_response(template, {})

def manage_security_groups_ssh(request):
    all_sec_groups = get_all_sgs() 
