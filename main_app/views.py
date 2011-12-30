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
    

def checkUpdates(request, row_limit):
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.method == "GET":
        try:
            user = request.user
            user.fielduserprofile
        except FieldUserProfile.DoesNotExist:
            return HttpResponse(status = 400)
        tasks = Task.objects.filter(fieldUser = user).order_by('last_modified')[:int(row_limit)]
        tasks = dict([(task.pk, task.version) for task in tasks ])
        json = simplejson.dumps(tasks)
        return HttpResponse(json, mimetype = "application/json")
    return HttpResponse(status = 400)


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
    
    
def editTaskState(request, task_id, state):
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.is_ajax() and request.method == "GET":
        if state not in ('0','1','2','3'):
            return HttpResponse(status = 400)
        try:
            task = Task.objects.get(pk = task_id)
        except Task.DoesNotExist:
            return HttpResponse(status = 400)
        if task.supervisor != request.user:
            return HttpResponse(status = 401)
        task.state = state
        task.save()
        return HttpResponse(status = 200)
    return HttpResponse(status = 400) 
    
#zadania dla danego uzytkownika terenowego (wszystkie lub okreslonego stanu)
    
def getUserTasks(request, field_user_id, opt_state = None):
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.is_ajax() and request.method == "GET":
        try:
            user = User.objects.get(pk = field_user_id)
            user.fielduserprofile
        except (FieldUserProfile.DoesNotExist, User.DoesNotExist):
            return HttpResponse(status = 400)

        tasks = Task.objects.filter(fieldUser = user)
        if opt_state:
            if opt_state not in ('0','1','2','3'):
                return HttpResponse(status = 400)
            tasks = tasks.filter(state = opt_state)
        tasks = dict([(task.pk, {
                                 "fu" : str(task.fieldUser),
                                 "lat" : str(task.latitude),
                                 "lon" : str(task.longitude),
                                 "state" : str(task.state),
                                 "name" : str(task.name),
                                 "desc" : str(task.description),
                                 "created" : str(task.creation_time),
                                 "modified" : str(task.last_modified),
                                 "finished" : str(task.finish_time),
                                 "started" : str(task.start_time),
                                 "ver" : str(task.version),
                                 "last_sync" : str(task.last_synced),
                                 }) for task in tasks]) #all task params
        
        json = simplejson.dumps(tasks)
        print json
        return HttpResponse(json, mimetype = "application/json") 
    return HttpResponse(status = 400)

            
        