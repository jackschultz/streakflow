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
from registration.views import RegistrationView
from forms import UserRegistrationForm
import pytz
from django.views.decorators.csrf import csrf_exempt


from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from django.utils.decorators import method_decorator
from registration import signals
from registration.models import RegistrationProfile
class MemberRegistrationView(RegistrationView):

  @method_decorator(csrf_exempt)
  def dispatch(self, *args, **kwargs):
    return super(MemberRegistrationView, self).dispatch(*args, **kwargs)
  
  def register(self, request, **cleaned_data):
    #return super(MemberRegistrationView, self).register(request,**cleaned_data)
    username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)
    new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                password, site)
    signals.user_registered.send(sender=self.__class__,
                                 user=new_user,
                                 request=request)
    return new_user
  

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
      goal.max_tf = goal.time_frames.all().latest()
      context['daily_goals'].append(goal)
    elif goal.time_frame_len == 'w':
      goal.max_tf = goal.time_frames.all().latest()
      context['weekly_goals'].append(goal)
    elif goal.time_frame_len == 'm':
      goal.max_tf = goal.time_frames.all().latest()
      context['monthly_goals'].append(goal)
  context['goals'] = goals
  context['daily_time'] = member.time_left_daily()
  context['weekly_time'] = member.time_left_weekly()
  context['monthly_time'] = member.time_left_monthly()
  return render_to_response('members/profile.html',context,context_instance=RequestContext(request))

def member_update(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('auth_login'))
  member = get_object_or_404(Member, user=request.user)
  context = {}
  context['member'] = member
  context['timezones'] = pytz.common_timezones
  if request.method == 'POST':
    timezone = request.POST.get('time_zone',None)
    email_reminder_time = request.POST.get('email_reminder_time',None)
    if timezone not in pytz.common_timezones or int(email_reminder_time) not in range(23):
      #fail right here and go back
      context = {}
      context['member'] = member
      context['timezones'] = pytz.common_timezones
      return render_to_response('members/update.html',context,context_instance=RequestContext(request))
    else:
      member.time_zone = timezone
      member.reminder_email_time = int(email_reminder_time)
      overall_email = request.POST.get('subscribed_overall_email',False)
      member.subscribed_overall_email = True if overall_email else False
      reminder_email = request.POST.get('subscribed_reminder_email',False)
      member.subscribed_reminder_email = True if reminder_email else False
      member.save()
      context = {}
      context['member'] = member
      context['timezones'] = pytz.common_timezones
      return render_to_response('members/update.html',context,context_instance=RequestContext(request))
  else:
    return render_to_response('members/update.html',context,context_instance=RequestContext(request))

def member_delete(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('auth_login'))
  member = get_object_or_404(Member, user=request.user)
  context = {}
  context['member'] = member
  if request.method == 'POST':
      delete_account= request.POST.get('delete_account',False)
      delete_account = True if delete_account else False
      if delete_account:
        member.user.delete()
      return HttpResponseRedirect(reverse('home'))
  else:
    return render_to_response('members/delete.html',context,context_instance=RequestContext(request))



