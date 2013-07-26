# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
from forms import GoalCreateForm
from models import Goal, TimeFrame, Objective
import datetime
import json
from streakflow.apps.members.models import Member


def goal_create(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('auth_login'))
  form = GoalCreateForm()
  if request.method == 'POST':
    form = GoalCreateForm(request.POST)
    if form.is_valid():
      #create the thing and 
      goal = form.save(commit=False)
      member = request.user.get_profile()
      goal.member = member
      goal.save()
      goal.update_timeframes()
      return HttpResponseRedirect(reverse('profile'))
    else:
      return render_to_response('goals/create.html',{'form':form},context_instance=RequestContext(request)) 
  else:
    context = {'form':form}
    return render_to_response('goals/create.html',context,context_instance=RequestContext(request))



#def objective_mark(request, goal_pk, tf_pk, obj_pk):
#  member = get_object_or_404(Member, user=request.user)
#  goal = get_object_or_404(Goal, pk=goal_pk)
#  if goal.member != member: #malicious or something
#    response_data['success'] = 'false'
#    raise Http404
#  if request.is_ajax():
#    response_data = {}
#    obj = get_object_or_404(Objective, pk=obj_pk)
#    obj.completed = not obj.completed
#    obj.save()
#    response_data['success'] = 'true'
#    if obj.completed:
#      response_data['completed'] = 'True'
#    else:
#      response_data['completed'] = 'False'
#    return HttpResponse(json.dumps(response_data), content_type='application/json')


def goal_overview(request, goal_pk):
  member = get_object_or_404(Member, user=request.user)
  goal = get_object_or_404(Goal, pk=goal_pk)
  if goal.member != member: #malicious or something
    response_data['success'] = 'false'
    raise Http404
  goal.update_timeframes()
  context = {}
  context['goal'] = goal
  return render_to_response('goals/overview.html',context,context_instance=RequestContext(request))














def goal_completed(request):
  '''
  The is the function that gets called when the person thinks that they have completed
  something in the time frame. We need to check if the person has completed it, 
  '''
  ##don't know if this is correct, but I think I need to make sure that the times are good and
  ##to not trust the updated things. I can just call update goal to begin with. Yeah...
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('login'))
  if request.is_ajax():
    response_data = {}
    #need to get the goal. Identified by id, make sure that no one else's id is in the way
    gid = request.POST['gid']
    member = get_object_or_404(Member, user=request.user)
    goal = Goal.objects.get(pk=gid)
    if goal.member != member: #malicious or something
      response_data['success'] = 'false'
      return HttpResponse(json.dumps(response_data), content_type='application/json')
    goal = goal_update(goal,member)
    state = check_goal_state(goal)
    if state == Status.COMPLETE:
      response_data['success'] = 'false'
      return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
      prev_complete = goal.num_completed_in_frame
      goal.num_completed_in_frame += 1
      if prev_complete + 1 == goal.times_in_frame:
        goal.consecutive += 1
      goal.last_completed = utc.localize(datetime.datetime.now())
      goal = goal_update(goal,member)
      context = {}
      context['goal'] = goal
      return render_to_response('goals/goal_view.html',context,context_instance=RequestContext(request))

def goal_edit(request, goal_pk):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('login'))
  member = get_object_or_404(Member, user=request.user)
  goal = get_object_or_404(Goal, pk=goal_pk)
  if goal.member != member: #malicious or something
    response_data['success'] = 'false'
    raise Http404
  #now we want to deal with the form
  form = GoalCreateForm()
  if request.method == 'POST':
    form = GoalCreateForm(request.POST)
    if form.is_valid():
      #now we need to make sure that the values are ok... not easier
      if not check_strength(goal, int(request.POST['times_in_frame']),request.POST['time_frame']):
        #we don't let them, probably should give a message.
        context = {'form':form}
        context['goal'] = goal
        return render_to_response('goals/edit.html',context,context_instance=RequestContext(request)) 
      goal.times_in_frame = int(request.POST['times_in_frame'])
      goal.time_frame = request.POST['time_frame']
      goal.save()
      return HttpResponseRedirect(reverse('profile'))
    else:
      context = {'form':form}
      context['goal'] = goal
      return render_to_response('goals/edit.html',context,context_instance=RequestContext(request)) 
  else:
    context = {'form':form}
    context['goal'] = goal
    return render_to_response('goals/edit.html',context,context_instance=RequestContext(request))
    #now they can modify it.
  context = {}
  context['goal'] = goal
  return render_to_response('goals/edit.html',context,context_instance=RequestContext(request))
  
def goal_delete(request, goal_pk):
  member = get_object_or_404(Member, user=request.user)
  goal = get_object_or_404(Goal, pk=goal_pk)
  if goal.member != member: #malicious or something
    response_data['success'] = 'false'
    raise Http404
  else:
    goal.delete()
  return HttpResponseRedirect(reverse('profile'))


