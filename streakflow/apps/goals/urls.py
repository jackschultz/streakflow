from django.conf.urls import patterns, url

urlpatterns = patterns('streakflow.apps.goals.views',
  url(r'^create$', 'goal_create', name='goal_create'),
  url(r'^completed$', 'goal_completed', name='goal_completed'),
  url(r'^(?P<goal_pk>\d+)$', 'goal_overview', name='goal_overview'),
  url(r'^(?P<goal_pk>\d+)/edit$', 'goal_edit', name='goal_edit'),
  url(r'^(?P<goal_pk>\d+)/delete$', 'goal_delete', name='goal_delete'),
)

