from rest_framework import serializers, permissions
from streakflow.apps.members.models import Member
from streakflow.apps.goals.models import Goal, TimeFrame, Objective

class ObjectiveSerializer(serializers.ModelSerializer):
  class Meta:
    model = Objective
    fields = ('id','completed')

class TimeFrameSerializer(serializers.ModelSerializer):
  objectives = ObjectiveSerializer(many=True)
  class Meta:
    model = TimeFrame
    fields = ('begin_time','end_time','objectives',)

  def asdf(self, goal):
    import pdb;pdb.set_trace()
    return goal.time_frames.latest()

class LatestTimeFrame(serializers.Field):
  def to_native(self,obj):
    latest = obj.latest()
    return TimeFrameSerializer(latest).data
  
class GoalSerializer(serializers.ModelSerializer):
  time_frames = LatestTimeFrame()
  
  class Meta:
    model = Goal
    fields =('goal_name','id','time_frame_len','num_per_frame','time_frames',)

  
class GoalOverviewSerializer(serializers.ModelSerializer):
  time_frames = TimeFrameSerializer(many=True, required=False)
  
  class Meta:
    model = Goal
    fields =('goal_name','id','time_frame_len','num_per_frame','time_frames',)



class MemberSerializer(serializers.ModelSerializer):
  goals = GoalSerializer(many=True)

  class Meta:
    model = Member



