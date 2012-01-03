from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    #web interface urls
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^login/$',  login, {'template_name': 'login.html'}),
    url(r'^create_task/$', 'main_app.views.createTask'),
    url(r'^edit_task_state/(?P<task_id>\d+)/(?P<state>\d)/$', 'main_app.views.editTaskState'),
    url(r'^get_user_tasks/(?P<field_user_id>\d+)/$', 'main_app.views.getUserTasks', name = "all"),
    url(r'^get_user_tasks/(?P<field_user_id>\d+)/(?P<opt_state>.*)/$', 'main_app.views.getUserTasks', name = "with_status"),
    
    #remote api urls
    
    url(r'^check_updates/(?P<row_limit>\d+)/$', 'main_app.api.checkUpdates'),
    url(r'^get_tasks/$', 'main_app.api.getTasks'),
    url(r'^get_tasks/(?P<opt_state>.*)/$', 'main_app.api.getTasks'),
    url(r'^task_finished/(?P<task_id>.*)/$', 'main_app.api.taskFinished'),
    url(r'^task_started/(?P<task_id>.*)/$', 'main_app.api.taskStarted'),
)
