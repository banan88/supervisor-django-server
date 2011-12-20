from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    url(r'^$', 'main_app.views.index'),
    (r'^login/$',  login, {'template_name': 'login.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^create_task/$', 'main_app.views.createTask'),
)
