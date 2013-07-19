from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

def home(request):
  context = {}
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse('profile'))
  return render_to_response('about.html',context,context_instance=RequestContext(request))

def about(request):
  context = {}
  return render_to_response('about.html',context,context_instance=RequestContext(request))
