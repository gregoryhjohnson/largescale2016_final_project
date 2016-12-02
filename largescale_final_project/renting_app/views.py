from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import ExtendedUserCreationForm,ProfileForm

# Create your views here.

@login_required
def home(request):
  #TODO: Placeholder. This should be a feed of items related to the user's intrests
  return HttpResponse('<h1>You are logged in, ' + request.user.first_name + '</h1>')

def register(request):
  if request.method == 'POST':
    user_form = ExtendedUserCreationForm(request.POST)

    if user_form.is_valid():
      new_user = user_form.save(commit=True)
      #Saving the user form automatically creates a corresponding profile object, query for it
      profile_instance = Profile.objects.get(pk=new_user.id)
      profile_form = ProfileForm(request.POST,instance=profile_instance)
      if profile_form.is_valid():
        profile_form.save()
  
      user = authenticate(username=new_user.username, password=user_form.clean_password2())
      if user is not None:
        login(request, user)
        return home(request)

    else:
      
      return render(request, 'renting_app/register.html',{
        'user_form': user_form,
        'profile_form': profile_form
      })

  #GET request, create and render new user and profile forms
  else:
   user_form = ExtendedUserCreationForm
   profile_form = ProfileForm
  
  return render(request, 'renting_app/register.html', {
    'user_form': user_form,
    'profile_form': profile_form    
  }) 

def user_login(request):
  #TODO
  return HttpResponse("Not Implemented")

