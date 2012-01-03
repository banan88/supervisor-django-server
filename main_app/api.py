from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils import simplejson
from main_app.models import *
from main_app.views import getTasksInJson
import simplejson
import base64


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
    
        
def checkUpdates(request, row_limit):
    if request.method == "GET":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        tasks = Task.objects.filter(fieldUser = user).order_by('last_modified')[:int(row_limit)]
        tasks = dict([(task.pk, task.version) for task in tasks ])
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


def taskStarted(request, task_id):
    if request.method == "GET":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        try:
            task = Tasks.objects.get(pk = task_id)
        except Task.DoesNotExist:
            return HttpResponse(status = 404)
        if task.fieldUser != user:
            return HttpResponse(status = 401)
        task.state = 2
        task.save()
    return HttpResponse(status = 200)

def taskFinished(request, task_id):
    pass