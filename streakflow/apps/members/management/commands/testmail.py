from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings
from mailsnake import MailSnake
from streakflow.apps.members.models import Member

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
      pass
     # mapi = MailSnake(settings.MANDRILL_API_KEY, api='mandrill')
     # subject = 'Streakflow updates!'
     # body = render_to_string('email/info1_email_body.txt')
     # import pdb;pdb.set_trace()
     # for member in Member.objects.filter(subscribed_reminder_email=True):
     #   print member
     #   print mapi.messages.send(message={'text':body, 'subject':subject, 'from_email':'info@streakflow.com', 'from_name':'Streakflow Information', 'to':[{'email':member.user.email, 'name':member.user.username}]})

