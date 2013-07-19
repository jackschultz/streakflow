from django.contrib.auth.models import User
from django.dispatch import receiver
from registration.signals import user_registered, user_activated
from django.db.models.signals import post_save
from models import Member

@receiver(user_registered)
def create_callback(sender, *args, **kwargs):
  user = kwargs['user']
  member = Member()
  member.user = user
  member.save()

@receiver(post_save,sender=User)
def create_profile(sender, **kwargs):
  user = kwargs['instance']

