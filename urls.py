from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    #web interface urls
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main_app.views.index'),
    url(r'^user_main/$', 'main_app.views.userMain'),
    url(r'^tasks/(?P<task_id>\d+)/$', 'main_app.views.taskDetails'),
    url(r'^task_history/(?P<task_id>\d+)/$', 'main_app.views.taskHistory'),
    url(r'^tasks/$', 'main_app.views.tasks'),
    url(r'^save_task/(?P<task_id>\d+)/$', 'main_app.views.saveTask'),
    url(r'^getusersuggestions/$', 'main_app.views.getUserSuggestions'),
    url(r'^getsupersuggestions/$', 'main_app.views.getSuperSuggestions'),
    url(r'^getnamesuggestions/$', 'main_app.views.getNameSuggestions'),
    url(r'^search/$', 'main_app.views.search'),
    url(r'^field_user/(?P<id>\d+)/$', 'main_app.views.fieldUser'),
    url(r'^field_user/$', 'main_app.views.fieldUsers'),
    url(r'^load_path/(?P<id>\d+)/$', 'main_app.views.loadPath'),
    url(r'^work_time/(?P<id>\d+)/$', 'main_app.views.workTime'),
    url(r'^new_task/$', 'main_app.views.newTask'),
    url(r'^search_user/$', 'main_app.views.searchUser'),
    url(r'^403/$', 'main_app.views.err403'),
    url(r'^add_user/$', 'main_app.views.add_user'),

    
    (r'^login/$',  login, {'template_name': 'login.html'}),
    (r'^logout/$', logout, {'next_page': '/'}),
    
    #remote api urls
    url(r'^get_n_tasks/(?P<count>\d+)/$', 'main_app.api.getNTasks'),
    url(r'^change_tasks_states/$', 'main_app.api.changeTasksStates'),
    url(r'^change_work_times/$', 'main_app.api.changeWorkTimes'),
    url(r'^get_tasks_since_last_sync/$', 'main_app.api.getTasksSinceLastSync'),
    url(r'^new_tasks_history/$', 'main_app.api.newTasksHistory'),
    url(r'^new_user_locations/$', 'main_app.api.newUserLocations'),
    #url(r'^get_task_state_table_version/$', 'main_app.api.getTaskStateTableVersion'),
    #url(r'^get_task_state_table_updates/$', 'main_app.api.getTaskStateTableUpdates')
)
