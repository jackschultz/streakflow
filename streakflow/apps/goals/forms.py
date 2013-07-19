from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import Goal

class GoalCreateForm(forms.ModelForm):
  class Meta:
    model = Goal
    exclude = ('member','consecutive','num_completed_in_frame','last_completed',)

