from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils import simplejson
from main_app.models import *
from django.views.decorators.csrf import csrf_exempt
import simplejson
import base64
import datetime


class CustomHeaderMiddleware(RemoteUserMiddleware):
    header = 'Authorization'


def basicAuth(request): #REDIRECT_HTTP_AUTHORIZATION - alwaysdata, HTTP_AUTHORIZATION - local
    try:
        credentials = base64.decodestring(request.META['HTTP_AUTHORIZATION'].split(' ', 1)[1]).split(":")
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
        tasks = tasks.order_by('last_modified')[:count]
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

@csrf_exempt
def changeTasksStates(request):
    if request.method == "POST":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        data = request.raw_post_data
        json = simplejson.loads(data)
        for entry in json:
            try:
                task = Task.objects.get(pk = int(entry.keys()[0]))
            except Task.DoesNotExist:
                continue
            if task.fieldUser != user:
                continue
            else:
                c_state = entry.get(entry.keys()[0])
                if not str(c_state) in ('2', '3'):
                    continue;
            task.state = c_state;
            task.save()

        return HttpResponse(status = 200)
    return HttpResponse(status = 400)


def postChangedDays(request): # json: [days {day} {} {} ]
    pass
