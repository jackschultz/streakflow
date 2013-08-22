from streakflow.apps.goals.models import Goal, TimeFrame, Objective
from streakflow.apps.members.models import Member
from serializers import GoalSerializer, GoalOverviewSerializer, MemberSerializer, TimeFrameSerializer, ObjectiveSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, exceptions, mixins
from permissions import IsOwner
from django.db.models import Max
import pytz


class GoalList(mixins.CreateModelMixin, APIView):
  model = Goal
 # permission_classes = (IsOwner,)

  def get(self, request, format=None):
    member = request.user.get_profile()
    goals = Goal.objects.filter(member=member)
    for goal in goals:
      goal.update_timeframes()
      goal.time_frames = [goal.time_frames.latest()]
      goal.consecutive = goal.consecutive_timeframes()
    serializer = GoalSerializer(goals, many=True)
    info = {}
    info['goals'] = serializer.data
    info['daily_time'] = member.time_left_daily()
    info['weekly_time'] = member.time_left_weekly()
    info['monthly_time'] = member.time_left_monthly()
    return Response(info)
  
  def post(self, request, format=None):
    data = request.DATA
    serializer = GoalSerializer(data=data)#, partial=True)
    if serializer.is_valid():
      serializer.object.member = self.request.user.get_profile()
      serializer.save()
      serializer.object.update_timeframes()
      serializer.object.consecutive = 0
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoalDetail(APIView):
  model = Goal
  permission_classes = (IsOwner,)

  def get_object(self, request, pk):
    try:
      goal = Goal.objects.get(pk=pk)
      member = request.user.get_profile()
      self.check_object_permissions(request, member)
      if goal.member != member:
        raise exceptions.PermissionDenied
      goal.update_timeframes()
      return goal
    except Goal.DoesNotExist:
      raise Http404

  def get(self, request, goal_pk, format=None):
    goal = self.get_object(request, goal_pk)
    serializer = GoalOverviewSerializer(goal)
    info = serializer.data
    info['consecutive'] = goal.consecutive_timeframes()
    return Response(info)

  def post(self, request, goal_pk, format=None):
    goal = self.get_object(request, goal_pk)
    serializer = GoalSterializer(goal, data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, goal_pk, format=None):
    goal = self.get_object(request, goal_pk)
    goal.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
 
class ObjectiveDetail(APIView):
  model = Objective
  permission_classes = (IsOwner,)

  def get_object(self, request, opk, gpk):
    try:
      member = request.user.get_profile()
      self.check_object_permissions(request, member)
      obj = Objective.objects.get(pk=opk)
      goal = Goal.objects.get(pk=gpk)
      #check both ownership things
      if obj.time_frame.goal.member != member:
        raise exceptions.PermissionDenied
      if obj.time_frame.goal != goal:
        raise exceptions.PermissionDenied
      return obj
    except Objective.DoesNotExist:
      raise Http404

  def get(self, request, goal_pk, obj_pk, format=None):
    obj = self.get_object(request, obj_pk, goal_pk)
    serializer = ObjectiveSerializer(obj)
    return Response(serializer.data)

  def post(self, request, goal_pk, obj_pk, format=None):
    obj = self.get_object(request, obj_pk, goal_pk)
    goal = Goal.objects.get(pk=goal_pk)
    serializer = ObjectiveSerializer(obj, data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      info = serializer.data
      info['consecutive'] = goal.consecutive_timeframes()
      info['all_complete'] = obj.time_frame.all_objs_finished()
      return Response(info)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQEST)

class MemberDetail(APIView):
  model = Member
  permission_classes = (IsOwner,)

  def get_object(self, request):
    try:
      member = request.user.get_profile()
      return member
    except Member.DoesNotExist:
      raise Http404

  def get(self, request, format=None):
    member = self.get_object(request)
    serializer = MemberSerializer(member)
    info = serializer.data
    info['timezones'] = pytz.common_timezones
    return Response(info)

