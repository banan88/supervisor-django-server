from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    url(r'^$', 'main_app.views.index'),
    (r'^login/$',  login, {'template_name': 'login.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^create_task/$', 'main_app.views.createTask'),
    url(r'^edit_task_state/(?P<task_id>\d+)/(?P<state>\d)/$', 'main_app.views.editTaskState'),
    url(r'^get_user_tasks/(?P<field_user_id>\d+)/$', 'main_app.views.getUserTasks', name = "all"),
    url(r'^get_user_tasks/(?P<field_user_id>\d+)/(?P<opt_state>.*)/$', 'main_app.views.getUserTasks', name = "with_status"),
    url(r'^check_updates/(?P<row_limit>\d+)/$', 'main_app.views.checkUpdates'),
)
