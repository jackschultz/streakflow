from django.conf.urls import patterns, url

urlpatterns = patterns('streakflow.apps.members.views',
  url(r'^$', 'member_profile', name='profile'),
  url(r'^update$', 'member_update', name='member_update'),
  url(r'^delete$', 'member_delete', name='member_delete'),
)
