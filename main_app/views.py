# -*- coding: utf-8 -*-

from django.shortcuts import *
from django.template.loader import render_to_string
from django.template import loader
from django.template.context import RequestContext
from django.template import Context, Template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import simplejson
from main_app.models import *
import datetime
from decimal import Decimal

# latitude +- 90 longitude +-180 - check to do

DESCRIPTIONS = {'0':'Anulowane', '1':'Oczekujące', '2':'Aktywne', '3':'Wykonane'}

def timeContext(request):
    return {'current_time': datetime.datetime.time(datetime.datetime.now())}


def isSupervisor(user): #check if user is not a fieldUser -> if he is, no access to web interface is granted
    try:
        user = FieldUserProfile.objects.get(user = user)
    except FieldUserProfile.DoesNotExist:
        test = True
    else:
        test = False
    return test



def index(request):
    return render_to_response('index.html', context_instance = RequestContext(request))


@login_required(login_url='/login/')
def userMain(request):
    if not isSupervisor(request.user):
        return HttpResponseRedirect('/403/')
    user = request.user
    tasks_created = Task.objects.filter(supervisor__pk = request.user.pk) #all created
    tasks_current = tasks_created.filter(state='2')
    tasks_pending = tasks_created.filter(state='1')
    tasks_done = tasks_created.filter(state='3')
    tasks_cancelled = tasks_created.filter(state='0')

    supervised_users_list = User.objects.filter(id__in =
            tasks_created.filter(state__in=['2','1'])
            .order_by('-date_modified')
            .values_list('fieldUser__id', flat=True)
        )
    size = supervised_users_list.count
    paginator = Paginator(supervised_users_list, 10)
    
    try:
        page = request.GET.get('page',1)
        supervised_users = paginator.page(page)
    except EmptyPage:
        supervised_users = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        supervised_users = paginator.page(1)
    return render_to_response('user_main.html', {
        'tasks_created':tasks_created.count(),
        'tasks_current':tasks_current.count(),
        'tasks_pending':tasks_pending.count(),
        'tasks_done':tasks_done.count(),
        'tasks_cancelled':tasks_cancelled.count(),
        'supervised_users':supervised_users,
        'size':size},
        context_instance = RequestContext(request))


@login_required(login_url='/login/')
def taskDetails(request, task_id):
    if not isSupervisor(request.user):
        return HttpResponseRedirect('/403/')
    try:
        task = Task.objects.get(pk = task_id)
    except Task.DoesNotExist:
        raise Http404
    curr_desc = DESCRIPTIONS[str(task.state)]
    return render_to_response('task_details.html', {'task':task, 'lat': str(task.latitude),
                    'lon': str(task.longitude), 'curr_desc':curr_desc}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def tasks(request):
    if not isSupervisor(request.user):
        return HttpResponseRedirect('/403/')
    tasks_list = Task.objects.all().order_by('-last_modified')
    size = tasks_list.count
    paginator = Paginator(tasks_list, 10)
    try:
        page = request.GET.get('page',1)
        tasks = paginator.page(page)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        tasks = paginator.page(1)
            
    return render_to_response('tasks.html', {'tasks':tasks, 'size':size}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def taskHistory(request, task_id):
    if not isSupervisor(request.user):
        return HttpResponseRedirect('/403/')
    try:
        task = Task.objects.get(pk = task_id)
    except Task.DoesNotExist:
        raise Http404
    tasks_history_base = TaskStateHistory.objects.filter(task__id = task.id).order_by('-change_time')
    print tasks_history_base.count()
    paginator = Paginator(tasks_history_base, 10)
    try:
        tasks_history = paginator.page(request.GET.get('page', 1))
    except EmptyPage:
        tasks_history = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        tasks_history = paginator.page(1)
    return render_to_response('task_history.html', {'task':task, 'tasks_history':tasks_history}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def getUserSuggestions(request):
    if not isSupervisor(request.user):
        return HttpResponse(status = 403)
    if request.is_ajax():
        if request.method == 'POST':
            q = request.POST.get('q')
            profiles = FieldUserProfile.objects.all()
            print 1
            try:
                profiles_queryset = profiles.filter(user__username__startswith=q)[:4]
            except (IndexError, User.DoesNotExist):
                print 'error'
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
    if not isSupervisor(request.user):
        return HttpResponse(status = 403)
    if request.is_ajax():
        if request.method == 'POST':
            q = request.POST.get('q')
            supers = User.objects.exclude(id__in = FieldUserProfile.objects.all().values_list('user__id', flat=True))
            try:
                supers = supers.filter(username__startswith=q)[:4]
            except (IndexError, User.DoesNotExist):
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
    if not isSupervisor(request.user):
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
    if not isSupervisor(request.user):
       return HttpResponseRedirect('/403/')
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
                try:
                    t_from = t_from.split('-')
                    print t_from
                    t_from = datetime.date(int(t_from[0]), int(t_from[1]), int(t_from[2]))
                    t_to = query.get('to', False)
                    t_to = t_to.split('-')
                    t_to = datetime.date(int(t_to[0]), int(t_to[1]), int(t_to[2]))
                    if t_from and t_to:
                        tasks = tasks.filter(last_modified__gte = t_from)
                        tasks = tasks.filter(last_modified__lte = t_to)
                except Exception:
                    raise Http404;
                print 'post time 0:'
                print tasks
            elif time == '1':
                date_n_ago = datetime.datetime.today() - datetime.timedelta(days=7)
                tasks = tasks.filter(last_modified__gte = date_n_ago)
                print 'post time 1:'
                print tasks
            elif time == '2':
                date_n_ago = datetime.datetime.today() - datetime.timedelta(days=1)
                tasks = tasks.filter(last_modified__gte = date_n_ago)
                print 'post time 2:'
                print tasks
            elif time == '3':
                tasks = tasks.filter(last_modified__gte = datetime.datetime.today())
                print 'post time 3:'
                print tasks
        print 'post all filters'
        tasks_list = tasks.order_by('-last_modified')
        size = tasks_list.count
        paginator = Paginator(tasks_list, 10)
        try:
            tasks = paginator.page(request.GET.get('page', 1))
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        print request.get_full_path()
        criteria = request.get_full_path().split('/')[-1] #to preserve get search params when paginating
        print criteria
        last_param =  criteria.split('&')[-1]
        print last_param
        if last_param[:4] == 'page':
            print 'in if'
            criteria = criteria.split('&')[:-1]
            criteria = '&'.join(criteria)
        print 'final url: ' + criteria
        return render_to_response('tasks.html', {'tasks':tasks, 'size':size, 'criteria':criteria}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def saveTask(request, task_id):
    if not isSupervisor(request.user):
        print 'lol0'
        return HttpResponse(status = 403)
    if request.is_ajax() and request.method == "POST":
        print 'lol'
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return HttpResponse(status = 400)
        json = request.POST
        print 'lol2'
        try:
            lat = Decimal(json.__getitem__("task_lat"))
            lon = Decimal(json.__getitem__("task_lon"))
        except ValueError:
            return HttpResponse(status = 400)
        if (lat > 85 or lat < -85) or (lon > 180 or lon < -180):
                return HttpResponse(status = 400)
        print 'lol3'
        name = json.__getitem__("task_name")
        desc = json.__getitem__("task_desc")
        t_user = json.__getitem__("task_user")
        state = json.__getitem__("task_state")
        was_edited = False
        tag = ""
        try:
            new_user = User.objects.get(username = t_user)
            print 2
            FieldUserProfile.objects.get(user = new_user)
        except (User.DoesNotExist, FieldUserProfile.DoesNotExist):
            return HttpResponse(status = 400)
        print task.longitude
        print lon
        print task.description
        print desc
        print "name: " + name

        if task.latitude != lat or \
        task.longitude != lon or \
        task.description != desc \
        or name != task.name:
            task.latitude = lat
            task.longitude = lon
            task.description = desc
            task.name = name
            was_edited = True
            tag = "zmieniono treść zadania. "
        print 11
        if state != task.state:
            task.state = state
            print state
            print task.state
            tag += "zmieniono stan zadania na \"%s\". " % (DESCRIPTIONS[str(state)])
            print 'hee'
        print 12
        if new_user != task.fieldUser:
            task.fieldUser = new_user
            tag += "zmieniono wykonawcę zadania na %s. " %(new_user)
        print 13
        try:
            task.save()
        except (InvalidOperation, Exception):
            return HttpResponse(status = 400)
            
        print "tag:" + tag
        print "was_edited" + str(was_edited)
        if was_edited or tag != "":
            print 'update history'
            task.updateTaskHistory(state, was_edited, request.user, datetime.datetime.now(), tag)
            print 'finish update'
        print "return"
        return HttpResponse(status = 200)
    return HttpResponse(status = 400)


def err403(request):
    return render_to_response('403.html', {}, context_instance = RequestContext(request))

def add_user(request):
    if(request.user.is_staff):
        return HttpResponseRedirect('/admin/main_app/fielduserprofile/add/');
    else:
        return render_to_response('non_staff_user.html', {}, context_instance = RequestContext(request));


@login_required(login_url='/login/')
def fieldUser(request, id):
    if not isSupervisor(request.user):
        return HttpResponseRedirect('/403/')
    try:
        fielduser = FieldUserProfile.objects.get(user__pk = id)
    except FieldUserProfile.DoesNotExist:
        raise Http404
    return render_to_response('fielduser.html', {'fielduser':fielduser, 'lat':str(fielduser.last_latitude),
            'lon':str(fielduser.last_longitude) }, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def fieldUsers(request):
    if not isSupervisor(request.user):
        return HttpResponseRedirect('/403/')
    fieldusers_list = FieldUserProfile.objects.all()
    paginator = Paginator(fieldusers_list, 10)
    size = fieldusers_list.count
    try:
        fieldusers = paginator.page(request.GET.get('page', 1))
    except EmptyPage:
        fieldusers = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        fieldusers = paginator.page(1)
    return render_to_response('fieldusers.html', {'fieldusers':fieldusers, 'size':size}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def loadPath(request, id):
    if not isSupervisor(request.user):
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


@login_required(login_url='/login/')
def workTime(request, id):
    if not isSupervisor(request.user):
        return HttpResponseRedirect('/403/')
    try:
        field_user = User.objects.get(pk = id)
    except User.DoesNotExist:
        return HttpResponse(status = 404)
    worktimes_base = WorkDay.objects.filter(fieldUser = field_user).order_by('-day')
    size = worktimes_base.count
    worktimes_list = list()
    for e in worktimes_base:
        sum = e.finish-e.start
        print sum
        e = {'day':e.day, 'start': e.start.time, 'finish': e.finish.time, 'sum':str(sum)}
        worktimes_list.append(e)
    paginator = Paginator(worktimes_list, 10 )
    try:
        worktimes = paginator.page(request.GET.get('page', 1))
    except EmptyPage:
        worktimese = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        worktimes = paginator.page(1)
    return render_to_response('work_times.html', {
        'worktimes': worktimes,
        'field_user':field_user,
        'size':size},
        context_instance = RequestContext(request))


@login_required(login_url='/login/')
def newTask(request):
    if not isSupervisor(request.user):
        return HttpResponseRedirect('/403/')
    if request.method == 'POST':
        tf = TaskForm(request.POST)
        tf.instance.supervisor = request.user
        print "state: " + tf.instance.state
        if(tf.is_valid()):
            task = tf.save()
            return HttpResponseRedirect('/tasks/'+str(task.pk) + '/')
    else:
        tf = TaskForm()
        tf.fields['fieldUser'].queryset = User.objects.filter(id__in =
            FieldUserProfile.objects.all()
            .values_list('user__id', flat=True))
    return render_to_response('new_task.html', {'tf':tf}, context_instance = RequestContext(request))


@login_required(login_url='/login/')
def searchUser(request):
    if not isSupervisor(request.user):
        return HttpResponseRedirect('/403/')
    if request.method == 'GET':
        query = request.GET
        name = query.get('name', False)
        if name:
            fieldusers = FieldUserProfile.objects.filter(user__username__icontains = name)
        else:
            fieldusers = []
    return render_to_response('searchUser.html', {'fieldusers':fieldusers}, context_instance = RequestContext(request))