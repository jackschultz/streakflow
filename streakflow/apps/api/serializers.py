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

class GoalSerializer(serializers.ModelSerializer):
  time_frames = TimeFrameSerializer(many=True, required=False)
#  time_frames = serializers.PrimaryKeyRelatedField(many=True)
  #time_frames = serializers.HyperlinkedRelatedField(many=True, view_name='TFDetail')
  
  class Meta:
    model = Goal
    fields =('goal_name','id','time_frame_len','num_per_frame','time_frames',)

  def pre_save(self, obj):
    pdb.set_trace()
    obj.member = self.request.user.get_profile()

class MemberSerializer(serializers.ModelSerializer):
  goals = GoalSerializer(many=True)

  class Meta:
    model = Member



