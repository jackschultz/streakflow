from django.contrib.auth.models import User
from django.dispatch import receiver
from registration.signals import user_registered, user_activated
from django.db.models.signals import post_save
from models import Member
from streakflow.apps.goals.models import Goal

@receiver(user_registered)
def create_callback(sender, *args, **kwargs):
  user = kwargs['user']
  member = Member()
  member.user = user
  member.save()
  #now we want to create a goal for this member,
  #so they have something and get goals
  goal = Goal(goal_name="Create more goals!",num_per_frame=1,time_frame_len='d')
  goal.member = member
  goal.save()

@receiver(post_save,sender=User)
def create_profile(sender, **kwargs):
  user = kwargs['instance']

