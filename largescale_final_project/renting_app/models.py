from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Profile(models.Model):
  user_id = models.BigIntegerField(primary_key=True)
  email = models.CharField(max_length=32, unique=True)
  first_name = models.CharField(max_length=32)
  last_name = models.CharField(max_length=32)
  zip_code = models.CharField(max_length=16)

class Category(models.Model):
  name = models.CharField(max_length=32)
  parent_category = models.ForeignKey('self')

class Item(models.Model):
  user_id = models.BigIntegerField(db_index=True)
  name = models.CharField(max_length=32)
  category = models.ForeignKey('Category')
  description = models.TextField()
  asking_price = models.DecimalField(max_digits=9, decimal_places=2)
  currently_rented = models.BooleanField()

class Rental(models.Model):
  user_id = models.BigIntegerField(db_index=True)
  item_id = models.BigIntegerField(db_index=True)
  start_date = models.DateField()
  end_date = models.DateField()
