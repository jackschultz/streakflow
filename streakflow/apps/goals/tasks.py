from celery import task
from models import Goal
from envelopes import Envelope
from streakflow.apps.members.models import Member
from django.template.loader import render_to_string
from django.conf import settings


@task() 
def check_goals_complete():
  pass

def send_reminder_email(member):
  '''
  Here we want to format the large amounts of info we could
  have on each person. Each should be sent 4 hours before the
  end of their day. For each goal, we want to send reminders
  for the following.
  '''
  pass
