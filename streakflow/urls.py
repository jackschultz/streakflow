from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from streakflow.apps.members.forms import UserRegistrationForm
from registration.backends.default.views import RegistrationView
from streakflow.apps.members.views import MemberRegistrationView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'streakflow.views.home', name='home'),
    url(r'^about$', 'streakflow.views.about', name='about'),
    url(r'^demo$', 'streakflow.views.demo', name='demo'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/register/$', 'streakflow.apps.members.views.register', name='registration_register'),
    #url(r'^accounts/register/$', 'registration.views.RegistrationView', kwargs={'form_class':UserRegistrationForm}, name='registration_register'),
    url(r'^accounts/register/$', MemberRegistrationView.as_view(form_class=UserRegistrationForm, success_url='registration_complete'),name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/', include('streakflow.apps.members.urls')),
    url(r'^goals/', include('streakflow.apps.goals.urls')),
    url(r'^api/', include('streakflow.apps.api.urls', namespace='rest_framework')),
)

urlpatterns += patterns('',
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token')
)


