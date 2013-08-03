from django.db import models
from django.db import IntegrityError
from django.db.models import Max
from streakflow.apps.members.models import Member
import datetime
import pytz
import calendar
import uuid
import pdb

# Create your models here.

DAILY = 'd'
WEEKLY = 'w'
MONTHLY = 'm'
TF_CHOICES = (
  (DAILY, 'Daily'),
  (WEEKLY, 'Weekly'),
  (MONTHLY, 'Monthly'),
)

class Goal(models.Model):
  member = models.ForeignKey(Member, related_name='goals')
  goal_name = models.CharField(max_length=50)
  num_per_frame = models.IntegerField(default=1)
  time_frame_len = models.CharField(max_length=1, choices=TF_CHOICES, default=DAILY)
  activated = models.BooleanField(default=True)
  started = models.DateTimeField(blank=True, auto_now_add=True)

  def save(self, *args, **kwargs):
    if not self.pk:
      while True:
        self.pk = int(str(uuid.uuid4().int)[0:6])
        try:
          super(Goal,self).save(*args, **kwargs)
          break
        except IntegrityError as e:
          raise e
          print e
          continue
    else:
      super(Goal,self).save(*args, **kwargs)

  def __unicode__(self):
    return self.goal_name

  def update_timeframes(self):
    #we want to go here and check to see if we have all the time frames
    #up to date here. 
    recent_time_frame = self.time_frames.all().aggregate(Max('end_time'))
    recent_time_frame = recent_time_frame['end_time__max']
    tz = self.member.time_zone
    if recent_time_frame is None:
      latest_date = datetime.datetime.now(pytz.timezone(tz)).date()
    else:
      latest_date = recent_time_frame
    cur_date = datetime.datetime.now(pytz.timezone(tz)).date()
    while cur_date >= latest_date:
      next_date = self.get_next_date(latest_date)
      tf = TimeFrame(num_per_frame=self.num_per_frame, begin_time=latest_date, end_time=next_date, goal=self)
      tf.save()
      latest_date = next_date

  def get_next_date(self, cur_date):
    if self.time_frame_len == DAILY:
      end_time = cur_date + datetime.timedelta(days=1)
    elif self.time_frame_len == WEEKLY:
      weekday = cur_date.weekday()
      end_time = cur_date - datetime.timedelta(days=weekday) + datetime.timedelta(days=7) 
    elif self.time_frame_len == MONTHLY:
      cur_month = cur_date.month
      cur_year = cur_date.year
      cur_day = cur_date.day
      days_in_month = calendar.monthrange(cur_year,cur_month)[1]
      end_time = cur_date - datetime.timedelta(days=cur_day) + datetime.timedelta(days=days_in_month+1) 
    return end_time

  def consecutive_timeframes(self):
    tfs = self.time_frames.all()
    consec = 0
    for tf in tfs[1:]:
      fini = tf.all_objs_finished()
      if fini:
        consec += self.num_per_frame
      else:
        break
    for obj in tfs[0].objectives.all():
      if obj.completed:
        consec += 1
    return consec

  def check_strength(self, nnpf, ntf):
  #returns true if the new requirements are tougher.
    if self.time_frame_len == DAILY:
      cur_freq = self.num_per_frame
    elif self.time_frame_len == WEEKLY:
      cur_freq = self.num_per_frame/7
    elif self.time_frame_len == MONTHLY:
      cur_freq = self.num_per_frame/28
    if ntf == DAILY:
      new_freq = nnpf 
    elif ntf == WEEKLY:
      new_freq = nnpf/7
    elif ntf == MONTHLY:
      new_freq = nnpf/28
    if new_freq >= cur_freq:
      return True 
    return False
 
class TimeFrame(models.Model):
  num_per_frame = models.IntegerField(default=1)
  begin_time = models.DateField(blank=True, default=None)
  end_time = models.DateField(blank=True, default=None)
  goal = models.ForeignKey(Goal, related_name='time_frames')

  class Meta:
    ordering = ('-begin_time',)
    get_latest_by = 'begin_time'
 

  def save(self, *args, **kwargs):
    if not self.pk:
      while True:
        self.pk = int(str(uuid.uuid4().int)[0:6])
        try:
          super(TimeFrame,self).save(*args, **kwargs)
          break
        except IntegrityError:
          continue
    else:
      super(TimeFrame,self).save(*args, **kwargs)
    if not self.objectives.all():
      #we need to create the objectives to show here
      for i in range(self.num_per_frame):
        obj = Objective(time_frame=self)
        obj.save()

  def __unicode__(self):
    return "%s - %s" % (self.begin_time.strftime('%B %d'),self.end_time.strftime('%B %d'))

  def all_objs_finished(self):
    fini = True
    for obj in self.objectives.all():
      if not obj.completed:
        fini = False
    return fini

class Objective(models.Model):
  time_completed = models.DateTimeField(blank=True, null=True, default=None)
  time_frame = models.ForeignKey(TimeFrame, related_name='objectives')
  completed = models.BooleanField(default=False)

  def save(self, *args, **kwargs):
    if not self.pk:
      while True:
        self.pk = int(str(uuid.uuid4().int)[0:6])
        try:
          super(Objective,self).save(*args, **kwargs)
          break
        except IntegrityError:
          continue
    else:
      super(Objective,self).save(*args, **kwargs)

  def __unicode__(self):
    return "OBJ"

