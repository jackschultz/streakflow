from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

def home(request):
  context = {}
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse('profile'))
  return render_to_response('about.html',context,context_instance=RequestContext(request))

def about(request):
  context = {}
  return render_to_response('about.html',context,context_instance=RequestContext(request))

def demo(request):
  context = {}
  return render_to_response('demo.html',context,context_instance=RequestContext(request))

def demo(request):
  context={}
  context['daily_goals'] = []
  context['weekly_goals'] = []
  context['monthly_goals'] = []
  goals = []
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
  return render_to_response('demo.html',context,context_instance=RequestContext(request))
