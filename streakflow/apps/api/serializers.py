from rest_framework import serializers, permissions
from streakflow.apps.members.models import Member
from streakflow.apps.goals.models import Goal, TimeFrame, Objective

class ObjectiveSerializer(serializers.ModelSerializer):
  class Meta:
    model = Objective

class TimeFrameSerializer(serializers.ModelSerializer):
  objectives = ObjectiveSerializer(many=True)
  class Meta:
    model = TimeFrame

class GoalSerializer(serializers.ModelSerializer):
  time_frames = TimeFrameSerializer(many=True)
  #time_frames = serializers.HyperlinkedRelatedField(many=True, view_name='TFDetail')
  
  class Meta:
    model = Goal
    fields =('goal_name','time_frames',)

class MemberSerializer(serializers.ModelSerializer):
  goals = GoalSerializer(many=True)

  class Meta:
    model = Member



