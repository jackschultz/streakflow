from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
import datetime
import uuid
import pytz
import calendar

# Create your models here.

class Member(models.Model):
  user = models.OneToOneField(User)
  time_zone = models.CharField(default='US/Eastern', max_length=30)
  subscribed_overall_email = models.BooleanField(default=True)
  subscribed_reminder_email = models.BooleanField(default=True)

  def save(self, *args, **kwargs):
    if not self.pk:
      while True:
        self.pk = int(str(uuid.uuid4().int)[0:6])
        try:
          super(Member,self).save(*args, **kwargs)
          break
        except IntegrityError as e:
          continue
    else:
      super(Member,self).save(*args, **kwargs)

  def __unicode__(self):
    return self.user.username

  def current_time(self):
    #we need to change all the timez here to the correct timezone
    member_tz = pytz.timezone(self.time_zone)
    cur_time = datetime.datetime.now(member_tz)
    return cur_time

  def time_left_daily(self):
    #we need to change all the timez here to the correct timezone
    member_tz = pytz.timezone(self.time_zone)
    cur_time = datetime.datetime.now(member_tz)
    end_date = cur_time.date()
    end_time = datetime.datetime.combine(end_date, datetime.time())+datetime.timedelta(days=1)
    end_time = member_tz.localize(end_time)
    return cur_time + (end_time - cur_time)

  def time_left_monthly(self):
    member_tz = pytz.timezone(self.time_zone)
    cur_time = datetime.datetime.now(member_tz)
    end_date = cur_time.date()
    cur_month = cur_time.month
    cur_year = cur_time.year
    cur_day = cur_time.day
    days_in_month = calendar.monthrange(cur_year,cur_month)[1]
    end_time = datetime.datetime.combine(end_date, datetime.time())-datetime.timedelta(days=cur_day)+datetime.timedelta(days=days_in_month+1) 
    end_time = member_tz.localize(end_time)
    return cur_time + (end_time - cur_time)

  def time_left_weekly(self):
    #we need to change all the timez here to the correct timezone
    member_tz = pytz.timezone(self.time_zone)
    cur_time = datetime.datetime.now(member_tz)
    end_date = cur_time.date()
    weekday = cur_time.weekday()
    end_time = datetime.datetime.combine(end_date, datetime.time())-datetime.timedelta(days=weekday)+datetime.timedelta(days=7) 
    end_time = member_tz.localize(end_time)
    return cur_time + (end_time - cur_time)
