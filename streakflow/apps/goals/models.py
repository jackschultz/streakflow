from django.db import models
from django.db import IntegrityError
from django.db.models import Max
from streakflow.apps.members.models import Member
import datetime
import pytz
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
    if recent_time_frame is None:
      latest_date = self.started.date()
    else:
      latest_date = recent_time_frame
    tz = self.member.time_zone
    cur_date = datetime.datetime.now(pytz.timezone(tz)).date()
    while cur_date >= latest_date:
      next_date = latest_date + datetime.timedelta(days=1)
      tf = TimeFrame(num_per_frame=self.num_per_frame, begin_time=latest_date, end_time=next_date, goal=self)
      tf.save()
      latest_date = next_date

class TimeFrame(models.Model):
  num_per_frame = models.IntegerField(default=1)
  begin_time = models.DateField(blank=True, default=None)
  end_time = models.DateField(blank=True, default=None)
  goal = models.ForeignKey(Goal, related_name='time_frames')

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
    return self.end_time.strftime('%A %B %d')

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

