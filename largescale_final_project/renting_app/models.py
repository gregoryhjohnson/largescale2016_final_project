from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models

# Create your models here.
class Profile(models.Model):
  user_id = models.BigIntegerField(primary_key=True)
  username = models.CharField(max_length=32, unique=True)
  email = models.CharField(max_length=32, unique=True)
  first_name = models.CharField(max_length=32)
  last_name = models.CharField(max_length=32)
  zip_code = models.CharField(max_length=16)
  registered_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.username

#Automatically create new Profile whenever a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
      print("new user created, creating new profile")
      profile_query = Profile.objects
      profile_query._hints = {'user_id': instance.id}
      profile_query.create(user_id=instance.id, email=instance.email,
          username= instance.username, first_name = instance.first_name,
          last_name = instance.last_name)
       
#Update the duplicated fields in Profile when user is updated 
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    #Tag query with user_id for routing
    profile_query = Profile.objects
    profile_query._hints = {'user_id' : instance.id}
    profile = profile_query.get(pk=instance.id)
    #Force profile to reflect changes made to these fields User, note: username cannot be changed
    profile.email=instance.email
    profile.first_name = instance.first_name
    profile.last_name = instance.last_name
    profile.save()

#This table should be replicated across db nodes
class Category(models.Model):
  name = models.CharField(max_length=32)
  parent_category = models.ForeignKey('self', null=True)

  def __str__(self):
    return self.name

class Item(models.Model):
  user_id = models.BigIntegerField(db_index=True)
  name = models.CharField(max_length=32)
  category = models.ForeignKey('Category')
  description = models.TextField()
  asking_price = models.DecimalField(max_digits=9, decimal_places=2)
  currently_rented = models.BooleanField()
  listed_date = models.DateField(auto_now_add=True)


class Rental(models.Model):
  user_id = models.BigIntegerField(db_index=True)
  item_id = models.BigIntegerField(db_index=True)
  start_date = models.DateField()
  end_date = models.DateField()
