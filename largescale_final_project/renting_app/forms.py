from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Item, Category

class ExtendedUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['zip_code',]

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['name', 'category', 'description', 'asking_price']

class SearchForm(forms.Form):
  searched = forms.CharField(label='Search term', max_length=100)
