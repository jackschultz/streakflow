# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Max
from models import Member
from streakflow.apps.goals.models import Goal
from utils import time_left_daily, time_left_weekly, time_left_monthly
import pytz
import pdb

def member_profile(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('auth_login'))
  #this should be slightly different. only now since not everyone has a 'member'
  member = get_object_or_404(Member, user=request.user)
  context={}
  context['daily_goals'] = []
  context['weekly_goals'] = []
  context['monthly_goals'] = []
  goals = Goal.objects.filter(member=member)
  for goal in goals:
    goal.update_timeframes()
    if goal.time_frame_len == 'd':
      goal.max_tf = goal.time_frames.all().order_by('-end_time')[0]
      context['daily_goals'].append(goal)
    elif goal.time_frame_len == 'w':
      goal.max_tf = goal.time_frames.all().order_by('-end_time')[0]
      context['weekly_goals'].append(goal)
    elif goal.time_frame_len == 'm':
      goal.max_tf = goal.time_frames.all().order_by('-end_time')[0]
      context['monthly_goals'].append(goal)
  context['goals'] = goals
  context['daily_time'] = time_left_daily(member)
  context['weekly_time'] = time_left_weekly(member)
  context['monthly_time'] = time_left_monthly(member)
  return render_to_response('members/profile.html',context,context_instance=RequestContext(request))

def member_update(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('auth_login'))
  member = get_object_or_404(Member, user=request.user)
  if request.method == 'POST':
    timezone = request.POST['time_zone']
    if timezone not in pytz.common_timezones:
      #fail right here and go back
      context = {}
      context['member'] = member
      context['timezones'] = pytz.common_timezones
      return render_to_response('members/update.html',context,context_instance=RequestContext(request))
    else:
      member.time_zone = timezone
      member.save()
      return HttpResponseRedirect(reverse('profile'))
  else:
    context = {}
    context['member'] = member
    context['timezones'] = pytz.common_timezones
    return render_to_response('members/update.html',context,context_instance=RequestContext(request))



