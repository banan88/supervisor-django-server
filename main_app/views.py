from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import loader
from django.template.context import RequestContext
from django.template import Context, Template

from django.contrib.auth.decorators import login_required
    
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
    return render_to_response("index.html", {}, context_instance = RequestContext(request))
    

def check_updates(request):
    json = simplejson.dumps({"a":123})
    return HttpResponse(json, mimetype = "application/json")

#tworzenie zadania, edycja zadania (zmiana stanu/parametrow)


def createTask(request):
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.is_ajax() and request.method == "POST":
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
            task.state = "1"
            task.name = name
            task.description = desc
            task.supervisor = request.user
        except KeyError:
            return HttpResponse(status = 400)
        task.save()
        return HttpResponse(status = 200)
    return HttpResponse(status = 400)
    
def cancelTask(request):
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.is_ajax() and request.method == "POST":
        json = request.POST
        try:
            id = json.__getitem__("id")
            try:
                task = Task.objects.get(pk = id)
            except Task.DoesNotExist:
                raise KeyError
        except KeyError:
            return HttpResponse(status = 400)
        if task.supervisor != request.user:
            return HttpResponse(status = 401)
        task.state = "0"
        task.save()
        print task.state
        return HttpResponse(status = 200)
    return HttpResponse(status = 400) 
    
#zadania dla danego uzytkownika terenowego (bez wzgledu na stan i to czy ten supervisor cos mu przydzielil)
    
def getUserTasks(request, field_user_id):
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.is_ajax() and request.method == "GET":
        try:
            print 1
            user = User.objects.get(pk = field_user_id)
            print 2
            try:
                user.fielduserprofile #https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
            except FieldUserProfile.DoesNotExist:
                print 3
                pass
                #return HttpResponse(status = 400)
        except User.DoesNotExist:
            return HttpResponse(status = 400)
        print "ok"
        tasks = Task.objects.filter(fieldUser = user)
        tasks = dict([(task.pk, {"name" : task.name}) for task in tasks]) #all task params
        #json = simplejson.dump
        print tasks
        return HttpResponse(status = 200) 
            
            
        