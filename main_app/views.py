# -*- coding: utf-8 -*-

from django.shortcuts import *
from django.template.loader import render_to_string
from django.template import loader
from django.template.context import RequestContext
from django.template import Context, Template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import simplejson
from main_app.models import *
import datetime

# latitude +- 90 longitude +-180 - check to do

DESCRIPTIONS = {'0':'Anulowane', '1':'Oczekujące', '2':'Aktywne', '3':'Wykonane'}

def timeContext(request):
    return {'current_time': datetime.datetime.time(datetime.datetime.now())}


def isSupervisor(request): #check if user is not a fieldUser -> if he is, no access to web interface is granted
    test = False
    try:
        user = FieldUserProfile.objects.get(user = request.user)
    except FieldUserProfile.DoesNotExist:
        test = True
    return test




def index(request):
    return render_to_response('index.html', context_instance = RequestContext(request))


@login_required(login_url='/login/')
def userMain(request):
    if not isSupervisor(request):
        return HttpResponse("403. nie masz uprawnien do interfejsu www.", status = 403)
    user = request.user
    tasks_created = Task.objects.filter(supervisor__pk = request.user.pk) #all created
    tasks_current = tasks_created.filter(state='2')
    tasks_pending = tasks_created.filter(state='1')
    tasks_done = tasks_created.filter(state='3')
    tasks_cancelled = tasks_created.filter(state='0')

    supervised_users = User.objects.filter(id__in =
            tasks_created.filter(state__in=['2','1'])
            .order_by('-date_modified')
            .values_list('fieldUser__id', flat=True)
        )
    paginator = Paginator(supervised_users, 10)
    
    try:
        page = paginator.page(request.GET.get('page', 1))
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except Exception, e:
        page = paginator.page(1)
    return render_to_response('user_main.html', {
        'tasks_created':tasks_created.count(),
        'tasks_current':tasks_current.count(),
        'tasks_pending':tasks_pending.count(),
        'tasks_done':tasks_done.count(),
        'tasks_cancelled':tasks_cancelled.count(),
        'supervised_users':supervised_users,
        'page':page},
        context_instance = RequestContext(request))


@login_required(login_url='/login/')
def taskDetails(request, task_id):
    if not isSupervisor(request):
        return HttpResponse("403. nie masz uprawnien do interfejsu www.", status = 403)
    try:
        task = Task.objects.get(pk = task_id)
    except Task.DoesNotExist:
        raise Http404
    curr_desc = DESCRIPTIONS[str(task.state)]
    return render_to_response('task_details.html', {'task':task, 'lat': str(task.latitude),
                    'lon': str(task.longitude), 'curr_desc':curr_desc}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def tasks(request):
    if not isSupervisor(request):
        return HttpResponse("403. nie masz uprawnien do interfejsu www.", status = 403)
    tasks = Task.objects.all().order_by('-last_modified')
    paginator = Paginator(tasks, 10)
    try:
        page = paginator.page(request.GET.get('page', 1))
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except Exception, e:
        page = paginator.page(1)
            
    return render_to_response('tasks.html', {'tasks':tasks, 'page':page}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def taskHistory(request, task_id):
    if not isSupervisor(request):
        return HttpResponse("403. nie masz uprawnien do interfejsu www.", status = 403)
    try:
        task = Task.objects.get(pk = task_id)
    except Task.DoesNotExist:
        raise Http404
    tasks_history = TaskStateHistory.objects.filter(task__id = task.id).order_by('-change_time')
    print tasks_history
    paginator = Paginator(tasks_history, 10)
    try:
        page = paginator.page(request.GET.get('page', 1))
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except Exception, e:
        page = paginator.page(1)
    return render_to_response('task_history.html', {'task':task, 'tasks_history':tasks_history, 'page':page}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def getUserSuggestions(request):
    if not isSupervisor(request):
        return HttpResponse(status = 403)
    if request.is_ajax():
        if request.method == 'POST':
            q = request.POST.get('q')
            profiles = FieldUserProfile.objects.all()
            print 1
            try:
                profiles_queryset = profiles.filter(user__username__startswith=q)[:4]
            except IndexError, User.DoesNotExist:
                pass
            print 2
            suggestions = []
            for u in profiles_queryset:
                suggestions.append(u.user.username)
            suggestions = dict(enumerate(suggestions))
            json = simplejson.dumps(suggestions)
            print json
            return HttpResponse(json, mimetype='application/json')
    return HttpResponse(status=400)

@login_required(login_url='/login/')
def getSuperSuggestions(request):
    if not isSupervisor(request):
        return HttpResponse(status = 403)
    if request.is_ajax():
        if request.method == 'POST':
            q = request.POST.get('q')
            supers = User.objects.exclude(id__in = FieldUserProfile.objects.all().values_list('user__id', flat=True))
            try:
                supers = supers.filter(username__startswith=q)[:4]
            except IndexError, User.DoesNotExist:
                pass
            print 2
            suggestions = []
            for u in supers:
                suggestions.append(u.username)
            suggestions = dict(enumerate(suggestions))
            json = simplejson.dumps(suggestions)
            print json
            return HttpResponse(json, mimetype='application/json')
    return HttpResponse(status=400)

@login_required(login_url='/login/')
def getNameSuggestions(request):
    if not isSupervisor(request):
        return HttpResponse(status = 403)
    if request.is_ajax():
        if request.method == 'POST':
            q = request.POST.get('q')
            tasks = Task.objects.all()
            try:
                tasks_queryset = tasks.filter(name__startswith=q)[:4]
            except IndexError:
                pass
            suggestions = []
            for t in tasks_queryset:
                suggestions.append(t.name)
            suggestions = dict(enumerate(suggestions))
            json = simplejson.dumps(suggestions)
            return HttpResponse(json, mimetype='application/json')
    return HttpResponse(status=400)
    

@login_required(login_url='/login/')
def search(request):
    if not isSupervisor(request):
        return HttpResponse("403. nie masz uprawnien do interfejsu www.", status = 403)
    if request.method == 'GET':
        query = request.GET
        tasks = Task.objects.all()
        name = query.get('name', False)
        if name:
            tasks = tasks.filter(name=name)
        username = query.get('user', False)
        try:
            fieldUser = User.objects.get(username =username)
        except User.DoesNotExist:
            username = False
        if username: #if user does not exist - ignore this search condition
            tasks = tasks.filter(fieldUser=fieldUser)
        print 'post userfilter'

        supername = query.get('super', False)
        try:
            print supername
            super = User.objects.get(username =supername)
            print 2
        except User.DoesNotExist:
            print 'doesnot'
            supername = False
        if supername: #if super does not exist - ignore this search condition
            print 3
            tasks = tasks.filter(supervisor=super)
            print 4
        state = query.get('state', False)
        if state:
            if not state == '4':
                tasks = tasks.filter(state=state)
        print 'post statefilter'           
        print tasks
        time = query.get('time', False)
        if time:
            if time == '0':
                t_from = query.get('from', False)
                t_from = t_from.split('-')
                print t_from
                t_from = datetime.date(int(t_from[0]), int(t_from[1]), int(t_from[2]))
                t_to = query.get('to', False)
                t_to = t_to.split('-')
                t_to = datetime.date(int(t_to[0]), int(t_to[1]), int(t_to[2]))
                if t_from and t_to:
                    tasks = tasks.filter(last_modified__gte = t_from)
                    tasks = tasks.filter(last_modified__lte = t_to)
                print 'post time 0:'
                print tasks
            elif time == '1':
                date_n_ago = datetime.datetime.today() - datetime.timedelta(days=7)
                tasks = tasks.filter(last_modified__gte = date_n_ago)
                print 'post time 1:'
                print tasks
            elif time == '2':
                date_n_ago = datetime.datetime.today() - timedelta(days=1)
                tasks = tasks.filter(last_modified__gte = date_n_ago)
                print 'post time 2:'
                print tasks
            elif time == '3':
                tasks = tasks.filter(last_modified__gte = datetime.datetime.today())
                print 'post time 3:'
                print tasks
        print 'post all filters'
        tasks = tasks.order_by('-last_modified')
        paginator = Paginator(tasks, 5)
        try:
            page = paginator.page(request.GET.get('page', 1))
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        except Exception, e:
            page = paginator.page(1)
        return render_to_response('tasks.html', {'tasks':tasks, 'page':page}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def saveTask(request, task_id):
    if not isSupervisor(request):
        return HttpResponse(status = 403)
    if request.is_ajax() and request.method == "POST":
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return HttpResponse(status = 400)
        json = request.POST
        try:
            lat = float(json.__getitem__("task_lat"))
            lon = float(json.__getitem__("task_lon"))
        except ValueError:
            return HttpResponse(status = 400)
        name = json.__getitem__("task_name")
        desc = json.__getitem__("task_desc")
        t_user = json.__getitem__("task_user")
        state = json.__getitem__("task_state")
        was_edited = False
        tag = ""
        print 1
        if task.latitude != lat or \
        task.longitude != lon or \
        task.description != desc \
        or name != task.name:
            task.latitude = lat
            task.longitude = lon
            task.description = desc
            task.name = name
            was_edited = True
            tag = "użytkownik %s zmienił treść zadania." % (request.user)
        if state != task.state:
            task.state = state
            tag += "użytkownik \"%s\" zmienił stan zadania na \"%s\"." % (request.user, DESCRIPTIONS[str(state)])
        task.save()
        print "ok"
        print "tag:" + tag
        print "was_edited" + str(was_edited)
        if was_edited or tag != "":
            print 'update history'
            task.updateTaskHistory(state, was_edited, request.user, datetime.datetime.now(), tag)
            print 'finish update'
        print "return"
        return HttpResponse(status = 200)
    return HttpResponse(status = 400)


@login_required(login_url='/login/')
def fieldUser(request, id):
    if not isSupervisor(request):
        return HttpResponse("403. nie masz uprawnien do interfejsu www.", status = 403)
    try:
        fielduser = FieldUserProfile.objects.get(user__pk = id)
    except FieldUserProfile.DoesNotExist:
        raise Http404
    return render_to_response('fielduser.html', {'fielduser':fielduser, 'lat':str(fielduser.last_latitude),
            'lon':str(fielduser.last_longitude) }, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def loadPath(request, id):
    if not isSupervisor(request):
        return HttpResponse(status = 403)
    if request.is_ajax() and request.method == "POST":
        try:
            fielduser = FieldUserProfile.objects.get(user__pk = id)
        except FieldUserProfile.DoesNotExist:
            return HttpResponse(status = 404)
        json = request.POST
        print json
        t_from = json.__getitem__("from")
        t_from = t_from.split('-')
        t_from = datetime.date(int(t_from[0]), int(t_from[1]), int(t_from[2]))
        t_to = json.__getitem__("to")
        t_to = t_to.split('-')
        t_to = datetime.date(int(t_to[0]), int(t_to[1]), int(t_to[2]))
        print t_to
        print fielduser.user.username
        locations = UserLocation.objects.filter(user = fielduser.user)
        locations = locations.filter(timestamp__gte=t_from)
        locations = locations.filter(timestamp__lte=t_to).order_by('-timestamp')
        location_list = []
        for l in locations:
            tmp = {'timestamp':str(l.timestamp), 'lat':str(l.latitude), 'lon':str(l.longitude)}
            location_list.append(tmp)
        json = simplejson.dumps(location_list)
        print json
        return HttpResponse(json, mimetype='application/json')

        