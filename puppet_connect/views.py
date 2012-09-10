# Create your views here.
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
import systems.models as system_models
import models as models
try:
    import json
except:
    from django.utils import simplejson as json
import yaml
def index(request):
    post_fact = request.POST.get('fact', None)
    if post_fact:
        fixed_fact = preprocess_yaml(post_fact)
        fact = yaml.load(fixed_fact)
        short_hostname = fact['values'].pop('hostname', None)
        fqdn = fact['values'].pop('fqdn', None)
        system = return_system(short_hostname, fqdn)
        for item in fact['values'].iterkeys():
            models.PuppetFact(system=system, fact=item, value=fact['values'][item]).save()
        return HttpResponse('OK')
    else:
        return HttpResponse('NO POST')
def preprocess_yaml(yaml_input):
    output = ""
    for entry in yaml_input.split("\n"):
        if not entry.strip().startswith('!') and not entry.strip().startswith('---'):
            output = "%s%s\n" % (output, entry)
    return output

def return_system(short_hostname, fqdn):
    try:
        system = system_models.System.objects.get(hostname=short_hostname)
        return system
    except system_models.System.DoesNotExist:
        try:
            system = system_models.System.objects.get(hostname=fqdn)
        except system_models.System.DoesNotExist:
            return None
        
