from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import Member
import pdb
from django.contrib.auth import authenticate, login, logout

class RegistrationForm(ModelForm):
  username = forms.CharField(label=(u'Username'))
  #no email right now
  password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
  password1 = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))

  class Meta:
    model = Member
    exclude = ('user',)

  def clean_username(self):
    username = self.cleaned_data['username']
    try:
      User.objects.get(username=username)
    except User.DoesNotExist:
      return username
    raise forms.ValidationError('That username is already taken. Please select another')

  def clean(self):
    password = self.cleaned_data['password']
    password1 = self.cleaned_data['password1']
    if password and password1 and password != password1:
      self._errors["password"] = self.error_class(["Jesus can't save people who can't repeat the same password..."])
      del self.cleaned_data["password"]
    return self.cleaned_data

class LoginForm(forms.Form):
  username = forms.CharField(label=(u'Username'))
  password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))

  def clean(self):
    username = self.cleaned_data['username']
    password = self.cleaned_data['password']
    if username and password:
      user_cache = authenticate(username=username, password=password)
      if not user_cache:
        self._errors["password"] = self.error_class(["Wrong username or password there champ"])
    return self.cleaned_data

