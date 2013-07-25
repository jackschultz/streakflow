from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from streakflow.apps.api import views

urlpatterns = patterns('streakflow.apps.goals.views',
  url(r'^goals$', views.GoalList.as_view()),
  url(r'^goals/(?P<goal_pk>\d+)$', views.GoalDetail.as_view()),
  url(r'^goals/(?P<goal_pk>\d+)/update/(?P<obj_pk>\d+)$', views.ObjectiveDetail.as_view()),
  url(r'^members/(?P<member_pk>\d+)$', views.MemberDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
