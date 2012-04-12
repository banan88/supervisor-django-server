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
    url(r'^save_task/(?P<task_id>\d+)/$', 'main_app.views.saveTask'),

    
    (r'^login/$',  login, {'template_name': 'login.html'}),
    (r'^logout/$', logout, {'next_page':'/'}),
    url(r'^create_task/$', 'main_app.views.createTask'),
    url(r'^edit_task_state/(?P<task_id>\d+)/(?P<state>\d)/$', 'main_app.views.editTaskState'),
    url(r'^get_user_tasks/(?P<field_user_id>\d+)/$', 'main_app.views.getUserTasks', name = "all"),
    url(r'^get_user_tasks/(?P<field_user_id>\d+)/(?P<opt_state>.*)/$', 'main_app.views.getUserTasks', name = "with_status"),
    
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
