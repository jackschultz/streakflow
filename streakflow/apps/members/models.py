from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
import datetime
import uuid

# Create your models here.

class Member(models.Model):
  user = models.OneToOneField(User)
  time_zone = models.CharField(default='US/Eastern', max_length=30)

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

