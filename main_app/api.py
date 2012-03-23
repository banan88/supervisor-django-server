from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils import simplejson
from main_app.models import *
from django.views.decorators.csrf import csrf_exempt
import simplejson
import base64
import datetime
from time import mktime
from settings import PRODUCTION
from django.utils.encoding import smart_str

class CustomHeaderMiddleware(RemoteUserMiddleware):
    header = 'Authorization'


def datetime_to_ms(dt):
    if dt == None or dt == 0:
        return 0
    a = int(1000*mktime(dt.timetuple()))
    #print a
    return a


def basicAuth(request): #REDIRECT_HTTP_AUTHORIZATION - alwaysdata, HTTP_AUTHORIZATION - local
    if PRODUCTION:
        auth_header = 'REDIRECT_HTTP_AUTHORIZATION'
    else:
        auth_header = 'HTTP_AUTHORIZATION'
    try:
        print 'ok'
        credentials = base64.decodestring(request.META[auth_header].split(' ', 1)[1]).split(":")
    except (KeyError, IndexError):
        return False
    user = authenticate(username = credentials[0], password = credentials[1])
    #user = authenticate(username = 'robol', password = 'robol')
    if user is None:
        return False
    try:
        user.fielduserprofile
    except FieldUserProfile.DoesNotExist:
        return False
    return user


def getNTasks(request, count):
    print "inside"
    if request.method == "GET":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        print 1
        tasks = Task.objects.filter(fieldUser = user)
        print 2
        tasks = tasks.order_by('last_modified')[:count]
        if len(tasks) == 0:
            return HttpResponse(status = 200)
        print 3
        tasks = [{"pk" : task.pk,
                                 "supervisor" : smart_str(task.supervisor),
                                 "lat" : smart_str(task.latitude),
                                 "lon" : smart_str(task.longitude),
                                 "state" : str(task.state),
                                 "name" : smart_str(task.name),
                                 "desc" : smart_str(task.description),
                                 "created" : datetime_to_ms(task.creation_time),
                                 "modified" : datetime_to_ms(task.last_modified),
                                 "finished" : datetime_to_ms(task.finish_time),
                                 "started" : datetime_to_ms(task.start_time),
                                 "ver" : repr(task.version),
                                 "last_sync" : datetime_to_ms(datetime.datetime.now()),
                                 } for task in tasks]

        print 4
        json = simplejson.dumps(tasks)
        print 5
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
        if len(tasks) == 0:
            return HttpResponse(status = 200)
        tasks = [{"pk" : task.pk,
                                 "supervisor" : smart_str(task.supervisor),
                                 "lat" : smart_str(task.latitude),
                                 "lon" : smart_str(task.longitude),
                                 "state" : str(task.state),
                                 "name" : smart_str(task.name),
                                 "desc" : smart_str(task.description),
                                 "created" : datetime_to_ms(task.creation_time),
                                 "modified" : datetime_to_ms(task.last_modified),
                                 "finished" : datetime_to_ms(task.finish_time),
                                 "started" : datetime_to_ms(task.start_time),
                                 "ver" : repr(task.version),
                                 "last_sync" : datetime_to_ms(datetime.datetime.now()),
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
                task = Task.objects.get(pk = int(entry[0]))
            except Task.DoesNotExist:
                continue
            if task.fieldUser != user:
                continue
            c_state = int(entry[1])
            if not (TaskState.objects.get(pk = c_state)).can_be_toggled:
                continue
            c_start_time = entry[2]
            if c_start_time != 0:
                task.start_time = datetime.datetime.fromtimestamp(c_start_time//1000) #POSIX timestamp s since 1970
                print 2
            c_finish_time = entry[3]
            if c_finish_time != 0:
                task.finish_time = datetime.datetime.fromtimestamp(c_finish_time//1000) #POSIX timestamp s since 1970
                print 3
            task.state = TaskState.objects.get(pk = c_state)
            task.save()
        user.fielduserprofile.sync_time = datetime.datetime.now()
        user.fielduserprofile.save()

        return HttpResponse(status = 200)
    return HttpResponse(status = 400)


@csrf_exempt
def changeWorkTimes(request):
    if request.method == "POST":
        user = basicAuth(request)
        if not user:
            return HttpResponse(status = 401)
        data = request.raw_post_data
        json = simplejson.loads(data)
        for entry in json:
            try:
                day = datetime.date(
                    int(entry[0][0:4]), int(entry[0][4:6]), int(entry[0][6:8]))
                workDay = WorkDay.objects.get(day = day)
            except WorkDay.DoesNotExist:
                workDay = WorkDay()
                workDay.fieldUser = user
                workDay.day = day;
            workDay.start = datetime.datetime.fromtimestamp(entry[1]//1000)
            workDay.finish = datetime.datetime.fromtimestamp(entry[2]//1000)
            workDay.save()
        return HttpResponse(status = 200)
    return HttpResponse(status = 400)

