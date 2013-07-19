from streakflow.apps.goals.models import Goal, TimeFrame, Objective
from streakflow.apps.members.models import Member
from serializers import GoalSerializer, MemberSerializer, TimeFrameSerializer, ObjectiveSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from permissions import IsOwner
import pdb

class GoalDetail(APIView):
  model = Goal
  permission_classes = (IsOwner,)

  def get_object(self, request, pk):
    try:
      goal = Goal.objects.get(pk=pk)
      member = request.user.get_profile()
      self.check_object_permissions(request, member)
      goal.update_timeframes()
      return goal
    except Goal.DoesNotExist:
      raise Http404

  def get(self, request, goal_pk, format=None):
    goal = self.get_object(request, goal_pk)
    serializer = GoalSerializer(goal)
    return Response(serializer.data)

  def put(self, request, goal_pk, format=None):
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
   
class TFDetail(APIView):
  model = TimeFrame
  permission_classes = (IsOwner,)

  def get_object(self, request, pk):
    try:
      member = request.user.get_profile()
      self.check_object_permissions(request, member)
      tf = TimeFrame.objects.get(pk=pk)
      return tf
    except TimeFrame.DoesNotExist:
      raise Http404

  def get(self, request, goal_pk, tf_pk, format=None):
    tf = self.get_object(request, tf_pk)
    serializer = TimeFrameSerializer(tf)
    return Response(serializer.data)

class ObjectiveDetail(APIView):
  model = Objective
  permission_classes = (IsOwner,)

  def get_object(self, request, pk):
    try:
      member = request.user.get_profile()
      self.check_object_permissions(request, member)
      obj = Objective.objects.get(pk=pk)
      return tf
    except Objective.DoesNotExist:
      raise Http404

  def get(self, request, goal_pk, tf_pk, obj_pk, format=None):
    obj = self.get_object(request, obj_pk)
    serializer = TimeFrameSerializer(obj)
    return Response(serializer.data)

  def put(self, request, goal_pk, tf_pk, obj_pk, format=None):
    obj = self.get_object(request, obj_pk)
    serializer = TimeFrameSerializer(obj, date=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQEST)

class ObjectiveList(APIView):
  model = Objective
  permission_classes = (IsOwner,)

  def get(self, request, goal_pk, tf_pk, format=None):
    member = request.user.get_profile()
    goals = Goal.objects.filter(member=member)
    serializer = GoalSerializer(goals, many=True)
    return Response(serializer.data)
  

class MemberDetail(APIView):
  model = Member
  permission_classes = (IsOwner,)

  def get_object(self, request, pk):
    try:
      member = Member.objects.get(pk=pk)
      member_request = request.user.get_profile()
      self.check_object_permissions(request, member)
      return member
    except Member.DoesNotExist:
      raise Http404

  def get(self, request, member_pk, format=None):
    member = self.get_object(request, member_pk)
    serializer = MemberSerializer(member)
    return Response(serializer.data)

class GoalList(APIView):
  model = Goal
  permission_classes = (IsOwner,)

  def get(self, request, format=None):
    member = request.user.get_profile()
    goals = Goal.objects.filter(member=member)
    for goal in goals:
      goal.update_timeframes()
    serializer = GoalSerializer(goals, many=True)
    return Response(serializer.data)
  
  def post(self, request, format=None):
    serializer = GoalSerializer(data=request.DATA)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
