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
    
    url(r'^get_n_tasks/(?P<count>\d+)/$', 'main_app.api.getNTasks'),
    url(r'^change_task_state/(?P<task_id>\d+)/(?P<task_state>\d)/$', 'main_app.api.changeTaskState'),
    url(r'^get_tasks_since_last_sync/$', 'main_app.api.getTasksSinceLastSync'),
    url(r'^get_last_sync_time/$', 'main_app.api.getLastSyncTime'),
)
