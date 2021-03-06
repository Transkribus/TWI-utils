from django import template
import re
from .utils import t_log
import logging
import settings
import os
import time

def appname(request):
    t_log("APPNAME: %s " % (request.resolver_match.app_name))
    return {'appname': request.resolver_match.app_name }

def urlname(request):
    return {'urlname': request.resolver_match.url_name }

def apphead(request):
    t_log("HEAD_TEMPLATE: %s " % (request.resolver_match.app_name))
    head_template = request.resolver_match.app_name+'/extra_head.html'
    t_log("HEAD_TEMPLATE: %s " % (head_template))

    try:
        template.loader.get_template(head_template) 
    except template.TemplateDoesNotExist:
        return {'apphead' : 'extra_head.html'} #fall back if no template available

    return {'apphead' : head_template}

def nav_up(request):
    #excptions for subverts
    if re.search(r'library\/\d+\/\d+\/\d+$', request.path):
        return {'nav_up' : re.sub(r'\/\d+\/\d+$',"",request.path)}
    if re.search(r'edit\/correct\/\d+\/\d+\/\d+$', request.path):
#        return {'nav_up' : re.sub(r'edit\/correct(\/\d+\/\d+)\/\d+$',r'library\1',request.path)}
#temp skip of doc page
        return {'nav_up' : re.sub(r'edit\/correct(\/\d+)\/\d+\/\d+$',r'library\1',request.path)}

    if re.search(r'edit\/correct\/\d+\/\d+$', request.path):
#temp skip of doc page
        return {'nav_up' : re.sub(r'edit\/correct(\/\d+)\/\d+$',r'library\1',request.path)}

    if re.search(r'dashboard\/\d+\/u\/.+$', request.path):
        return {'nav_up' : re.sub(r'\/u\/.+$',"",request.path)}
    
    t_log("CONTEXT NAV_UP %s" % request.path, logging.WARN)
    
    nav_up = re.sub(r'\/[^\/]+$',"/",request.path)
    if nav_up == request.path :
        return {'nav_up': None}

    return {'nav_up': re.sub(r'\/[^\/]+$',"/",request.path)}

def version(request):
    return {'version': settings.VERSION, 'milestone': settings.MILESTONE, 'deploy_time': time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(settings.BASE_DIR+'/wsgi.py'))) }

def browser_list(request):
    return {'BROWSERS' : settings.BROWSERS}


