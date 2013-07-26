import datetime
import pytz
import calendar
from models import Member

def time_left_daily(member):
  #we need to change all the timez here to the correct timezone
  member_tz = pytz.timezone(member.time_zone)
  cur_time = datetime.datetime.now(member_tz)
  end_date = cur_time.date()
  end_time = datetime.datetime.combine(end_date, datetime.time())+datetime.timedelta(days=1)
  end_time = member_tz.localize(end_time)
  return cur_time + (end_time - cur_time)

def time_left_monthly(member):
  member_tz = pytz.timezone(member.time_zone)
  cur_time = datetime.datetime.now(member_tz)
  end_date = cur_time.date()
  cur_month = cur_time.month
  cur_year = cur_time.year
  cur_day = cur_time.day
  days_in_month = calendar.monthrange(cur_year,cur_month)[1]
  end_time = datetime.datetime.combine(end_date, datetime.time())-datetime.timedelta(days=cur_day)+datetime.timedelta(days=days_in_month) 
  end_time = member_tz.localize(end_time)
  return cur_time + (end_time - cur_time)

def time_left_weekly(member):
  #we need to change all the timez here to the correct timezone
  member_tz = pytz.timezone(member.time_zone)
  cur_time = datetime.datetime.now(member_tz)
  end_date = cur_time.date()
  weekday = cur_time.weekday()
  end_time = datetime.datetime.combine(end_date, datetime.time())-datetime.timedelta(days=weekday)+datetime.timedelta(days=7) 
  end_time = member_tz.localize(end_time)
  return cur_time + (end_time - cur_time)
