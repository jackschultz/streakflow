from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'streakflow.views.home', name='home'),
    url(r'^about$', 'streakflow.views.about', name='about'),
    url(r'^demo$', 'streakflow.views.demo', name='demo'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/', include('streakflow.apps.members.urls')),
    url(r'^goals/', include('streakflow.apps.goals.urls')),
    url(r'^api/', include('streakflow.apps.api.urls', namespace='rest_framework')),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
