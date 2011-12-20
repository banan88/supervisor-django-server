from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import loader
from django.template.context import RequestContext
from django.template import Context, Template
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt        
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import simplejson
from main_app.models import *
import simplejson


def validateLat(value):
    value = float(value)
    if value > 180 or value < -180:
        value = float(value)
        raise KeyError
    return value
    
    
def validateLon(value):
    value = float(value)
    if value > 90 or value < -90:
        raise KeyError
    return value

def index(request):
    return render_to_response('index.html', {}, context_instance = RequestContext(request))
    

def check_updates(request):
    json = simplejson.dumps({'a':123})
    return HttpResponse(json, mimetype = 'application/json')

#tworzenie zadania, edycja zadania (zmiana stanu/parametrow)


def createTask(request):
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.is_ajax() and request.method == 'POST':
        json = request.POST
        try:
            fuser = json.__getitem__("fuser")
            lat = json.__getitem__("lat")
            lon = json.__getitem__("lon")
            name = json.__getitem__("name")
            desc = json.__getitem__("desc")
        
            task = Task()

            try:
                task.fieldUser = User.objects.get(pk = fuser)
            except User.DoesNotExist:
                raise KeyError

            task.latitude = validateLat(lat)
            task.longitude = validateLon(lon)
            task.state = '1'
            task.name = name
            task.description = desc
            task.supervisor = request.user
        except KeyError:
             return HttpResponse(status = 400)
        task.save()
        return HttpResponse(task)
    else:
        return HttpResponse(status = 400) #bad request header