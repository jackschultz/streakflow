from celery import task
from models import Member
from streakflow.apps.goals.models import Goal
from django.template.loader import render_to_string
from django.conf import settings
from mailsnake import MailSnake
import datetime


@task
def reminder_emails():
  print "DOING EMAILS NOW"
  mapi = MailSnake(settings.MANDRILL_API_KEY, api='mandrill')
  #get the context for this...
  context = {}
  members = Member.objects.filter(subscribed_reminder_email=True)
  #now we want to filter members for the correct reminder time that they want.


  for member in members:
    hour = member.reminder_email_time
    minute = 0
    mem_time = member.current_time()
    mem_time_hour = mem_time.hour
    mem_time_minute = mem_time.minute/30 * 30 #deals with how long it takes to go through all
    if mem_time_hour != hour or mem_time_minute != minute: #this is the check for if we send the email. Currently, we want to
      continue
    context['username'] = member.user.username
    print "Sending for " + member.user.username
    #daily goals
    context['daily_goals'] = []
    daily_goals = member.goals.filter(time_frame_len='d')
    for goal in daily_goals:
      goal.max_tf = goal.time_frames.all().latest()
      #here we should get the number and number left
      goal.finished = goal.max_tf.num_objs_finished()
      if goal.finished < goal.num_per_frame:
        context['daily_goals'].append(goal)
    context['daily_time'] = member.time_left_daily()

    #weekly goals
    context['weekly_goals'] = []
    weekly_goals = member.goals.filter(time_frame_len='w')
    weekly_time = member.time_left_weekly()
    context['weekly_time'] = weekly_time
    days_left_weekly = (weekly_time - member.current_time()).days
    for goal in weekly_goals:
      goal.max_tf = goal.time_frames.all().latest()
      #here we should get the number and number left
      goal.finished = goal.max_tf.num_objs_finished()
      goal_difference = goal.num_per_frame - goal.finished
      under_week_deadline = True if goal_difference > days_left_weekly else False #or less than equal....
      if under_week_deadline:
        context['weekly_goals'].append(goal)

    #monthly goals
    context['monthly_goals'] = []
    monthly_goals = member.goals.filter(time_frame_len='m')
    monthly_time = member.time_left_monthly()
    context['monthly_time'] = monthly_time
    days_left_monthly = (monthly_time - member.current_time()).days
    for goal in monthly_goals:
      goal.max_tf = goal.time_frames.all().latest()
      #here we should get the number and number left
      goal.finished = goal.max_tf.num_objs_finished()
      goal_difference = goal.num_per_frame - goal.finished
      under_month_deadline = True if goal_difference > days_left_monthly else False #or less than equal....
      if under_month_deadline:
        context['monthly_goals'].append(goal)      
    
    if context['monthly_goals'] or context['weekly_goals'] or context['daily_goals']:
      subject = render_to_string('goals/reminder_email_subject.txt')
      body = render_to_string('goals/reminder_email_body.txt', context)
      print mapi.messages.send(message={'text':body, 'subject':subject, 'from_email':'reminders@streakflow.com', 'from_name':'Streakflow Reminders', 'to':[{'email':member.user.email, 'name':member.user.username}]})
