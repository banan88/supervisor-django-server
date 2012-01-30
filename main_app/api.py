from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils import simplejson
from main_app.models import *
from main_app.views import getTasksInJson
from datetime import datetime
import simplejson
import base64
import datetime


class CustomHeaderMiddleware(RemoteUserMiddleware):
    header = 'Authorization'


def basicAuth(request):
    try:
        credentials = base64.decodestring(request.META['HTTP_AUTHORIZATION'].split(' ')[1]).split(":")
    except KeyError:
        return False
    user = authenticate(username = credentials[0], password = credentials[1])
    if user is None:
        return False
    try:
        user.fielduserprofile
    except FieldUserProfile.DoesNotExist:
        return False
    return user


def getNTasks(request, count):
    if request.method == "GET":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        tasks = Task.objects.filter(fieldUser = user)
        tasks = tasks.order_by('last_modified')
        tasks = [{"pk" : task.pk,
                                 "supervisor" : str(task.supervisor),
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
                                 "last_sync" : str(datetime.datetime.now()),
                                 } for task in tasks]
        json = simplejson.dumps(tasks)
        user.fielduserprofile.sync_time = datetime.datetime.now()
        user.fielduserprofile.save()
        return HttpResponse(json, mimetype = "application/json") 
    return HttpResponse(status = 400)
    

def getTasksSinceLastSync(request):
    if request.method == "GET":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        tasks = Task.objects.filter(fieldUser = user)
        tasks = tasks.filter(last_modified__gte=user.fielduserprofile.sync_time)
        tasks = [{"pk" : task.pk,
                                 "supervisor" : str(task.supervisor),
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
                                 "last_sync" : str(datetime.datetime.now()),
                                 } for task in tasks]
        json = simplejson.dumps(tasks)
        user.fielduserprofile.sync_time = datetime.datetime.now()
        user.fielduserprofile.save()
        return HttpResponse(json, mimetype = "application/json") 
    return HttpResponse(status = 400)


def changeTaskState(request, task_id, task_state):
    if request.method == "GET":
        if not task_state in ('1', '2', '3'):
            return HttpResponse(status = 401)
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        try:
            task = Task.objects.get(pk = task_id)
        except Task.DoesNotExist:
            return HttpResponse(status = 404)
        if task.fieldUser != user:
            return HttpResponse(status = 401)
        
        task.state = task_state
        task.save()
        return HttpResponse(status = 200)
    return HttpResponse(status = 400)

def getLastSyncTime(request):
    if request.method == "GET":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        json = simplejson.dumps(str(user.fielduserprofile.sync_time))
        print json
        return HttpResponse(json, mimetype = "application/json")
    return HttpResponse(status = 400)

def setStartTime(request, time):
    pass

def setFinishTime(request, time):
    pass
