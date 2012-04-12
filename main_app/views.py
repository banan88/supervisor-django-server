# -*- coding: utf-8 -*-

from django.shortcuts import *
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
from datetime import datetime


DESCRIPTIONS = {'0':'Anulowane', '1':'Oczekujące', '2':'Aktywne', '3':'Wykonane'}

def timeContext(request):
    return {'current_time': datetime.time(datetime.now())}


def index(request):
    return render_to_response('index.html', context_instance = RequestContext(request))

def userMain(request):
    if request.user.is_authenticated():
        user = request.user
        return render_to_response('user_main.html', {'task_details':False}, context_instance = RequestContext(request))
    else:
        return redirect('/login/')

def taskDetails(request, task_id):
    try:
        task = Task.objects.get(pk = task_id)
    except Task.DoesNotExist:
        raise Http404
    curr_desc = DESCRIPTIONS[str(task.state)]
    if request.user.is_authenticated():
        return render_to_response('user_main.html', {'task_details':True, 'task':task, 'curr_desc':curr_desc}, context_instance = RequestContext(request))

def saveTask(request, task_id):
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.is_ajax() and request.method == "POST":
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return HttpResponse(status = 400)
        json = request.POST
        lat = float(json.__getitem__("task_lat"))
        lon = float(json.__getitem__("task_lon"))
        name = json.__getitem__("task_name")
        desc = json.__getitem__("task_desc")
        t_user = json.__getitem__("task_user")
        state = json.__getitem__("task_state")
        was_edited = False
        tag = ""
        if task.latitude != lat or \
        task.longitude != lon or \
        task.description != desc \
        or name != task.name:
            task.latitude = lat
            task.longitude = lon
            task.description = desc
            task.name = name
            was_edited = True
            tag = "użytkownik %s zmienił zawartość zadania." % (request.user)
        if state != task.state:
            task.state = state
            tag += "użytkownik \"%s\" zmienił stan zadania na \"%s\"." % (request.user, DESCRIPTIONS[str(state)])
        task.save()
        print "ok"
        print tag
        print was_edited
        if was_edited or tag != "":
            task.updateTaskHistory(task, state, was_edited, request.user, datetime.now(), tag)
        return HttpResponse(status = 200)
    return HttpResponse(status = 400)

#def updateTaskHistory(self, task, new_state, was_content_edited, user, timestamp, tag):


def getTasksInJson(user, opt_state):
    tasks = Task.objects.filter(fieldUser = user)
    if opt_state:
        if opt_state not in ('0','1','2','3'):
            return HttpResponse(status = 400)
        tasks = tasks.filter(state = opt_state)
    tasks = [{"pk" : task.pk,
                             "supervisor" : str(task.supervisor),
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
                             } for task in tasks] #all task params
    json = simplejson.dumps(tasks)
    return HttpResponse(json, mimetype = "application/json") 


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

            task.latitude = lat
            task.longitude = lon
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
    if request.method == "GET":
        try:
            user = User.objects.get(pk = field_user_id)
            user.fielduserprofile
        except (FieldUserProfile.DoesNotExist, User.DoesNotExist):
            return HttpResponse(status = 400)
        return getTasksInJson(user = user, opt_state = opt_state)
    return HttpResponse(status = 400)

