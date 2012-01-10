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
    
        
def checkUpdates(request, row_limit = 100):
    if request.method == "GET":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        tasks = Task.objects.filter(fieldUser = user).order_by('last_modified')[:int(row_limit)]
        tasks = [{ "pk" : task.pk, "version" : task.version } for task in tasks ]
        json = simplejson.dumps(tasks)
        return HttpResponse(json, mimetype = "application/json")
    return HttpResponse(status = 400)


def getChangedTasks(request): #should take json object with primary keys
    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.method == "GET":
        pass #should return requested task objects 
    return HttpResponse(status = 400)

    if not request.user.is_authenticated():
        return HttpResponse(status = 401)
    if request.method == "GET":
        try:
            user = User.objects.get(pk = field_user_id)
            user.fielduserprofile
        except (FieldUserProfile.DoesNotExist, User.DoesNotExist):
            return HttpResponse(status = 400)


def getTasks(request, opt_state = None):
    if request.method == "GET":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        return getTasksInJson(user, opt_state)
    return HttpResponse(status = 400)

def getTasksSince(request, datestring):
    if request.method == "GET":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        tasks = Task.objects.filter(fieldUser = user)
        datelist = datestring.split('X')
        if len(datelist) != 7:
            return HttpResponse(status = 400)
        date = datetime.date(int(datelist[0]), int(datelist[1]), int(datelist[2]))
        time = datetime.time(int(datelist[3]), int(datelist[4]), int(datelist[5]), int(datelist[6]))
        dt = datetime.datetime.combine(date, time)
        tasks = tasks.filter(last_modified__gte=dt)
        for task in tasks:
            print "dt:" + str(dt)
            print "task" + str(task.last_modified)
        tasks = [{"pk" : task.pk,
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
        return HttpResponse(json, mimetype = "application/json")
    return HttpResponse(status = 400)
