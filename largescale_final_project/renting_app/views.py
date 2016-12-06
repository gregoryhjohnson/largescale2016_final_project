from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import ExtendedUserCreationForm,ProfileForm, ItemForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect

# Create your views here.

#Index for users who are not logged in
def index(request):
  if request.user.is_authenticated():
    return home(request)
  else:
    return user_login(request)
  #return HttpResponse('<h1>You are not logged in<h1>')

@login_required
def home(request):

  #TODO: Placeholder. This should be a feed of items related to the user's intrests
  item_list = Item.objects.filter(currently_rented=False).order_by('-listed_date')
  for item in item_list:
    item.user = Profile.objects.get(pk=item.user_id)

  context = {
    'item_list': item_list,
    'user': request.user.first_name,
    'user_id': request.user.id
  }
  return render(request, 'renting_app/home.html', context)

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
        'profile_form': ProfileForm,
        'user_id': request.user.id
      })

  #GET request, create and render new user and profile forms
  else:
   user_form = ExtendedUserCreationForm
   profile_form = ProfileForm
  
  return render(request, 'renting_app/register.html', {
    'user_form': user_form,
    'profile_form': profile_form,
    'user_id': request.user.id  
  }) 

def user_login(request):
  #If already logged in just redirect to home page
  if request.user.is_authenticated():
    return HttpResponseRedirect('/renting_app')

  if request.method == 'POST':
    auth_form = AuthenticationForm(data=request.POST)

    if auth_form.is_valid():
      login(request, auth_form.get_user())
      return HttpResponseRedirect('/renting_app/')

  auth_form = AuthenticationForm
  return render(request, 'renting_app/login.html', {
    'auth_form': auth_form,
    'user_id': request.user.id
  })
  
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/renting_app/home')

@login_required
def profile(request, user_id):
  if not request.user.is_authenticated():
    return user_login(request)

  user = User.objects.get(pk=user_id)
  profile = Profile.objects.get(pk=user_id)

  #Tag query with user_if for db routing
  item_query = Item.objects
  item_query._hints = {'user_id' : user_id}

  items = item_query.filter(user_id=user_id).order_by('-listed_date')
  paginator = Paginator(items, 10)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    posts = paginator.page(1) 
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    posts = paginator.page(paginator.num_pages)

  my_profile = False
  if int(request.user.id) == int(user_id):
    my_profile = True
 


  context = {
    
    'user' : user,
    'email' : profile.email,
    'first_name' : profile.first_name,
    'last_name' : profile.last_name,
    'zip_code' : profile.zip_code,
    'posts' : posts,
    'user_id': request.user.id,
    'my_profile': my_profile
    
  }
  return render(request, 'renting_app/profile.html', context)

@login_required
def add(request):
  if request.method == 'POST':
    item_form = ItemForm(request.POST)



    if item_form.is_valid():
      new_item = item_form.save(commit=False)
      new_item.user_id = request.user.id
      new_item.currently_rented = False
      new_item.save()

      return redirect('/renting_app/home/')

    else:
      
      return render(request, 'renting_app/add.html',{
        'item_form': item_form
      })

  else:
   item_form = ItemForm
  
  return render(request, 'renting_app/add.html', {
    'item_form': item_form,
    'user_id': request.user.id  
  }) 

@login_required
def modify(request):
  if request.method == 'POST':
    delete = request.POST.getlist('delete')
    rented = request.POST.getlist('rented')
    returned = request.POST.getlist('returned')
    
    for rent_id in returned:
      item = Item.objects.get(id=rent_id)
      item.currently_rented = False
      item.save()
    for rent_id in rented:
      item = Item.objects.get(id=rent_id)
      item.currently_rented = True
      item.save()
    for delete_id in delete:
      item = Item.objects.get(id=delete_id)
      item.delete()
    url = '/renting_app/profile/' + str(request.user.id)
    return HttpResponseRedirect(url)


@login_required
def item(request, item_id):
  item = Item.objects.get(id=item_id)
  item_user = Profile.objects.get(pk=item.user_id)
    
  return render(request, 'renting_app/item.html', {'item' : item, 'user_id': request.user.id, "item_user": item_user})
