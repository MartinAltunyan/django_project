from __future__ import unicode_literals
from django.db import models

class User(models.Model):
	first_name = models.CharField(max_length=50)
	alias = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	date=models.DateField()
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
class Product(models.Model):
    name=models.CharField(max_length=255)
    
    user=models.ForeignKey(User, related_name='user_product')
    favorites=models.ManyToManyField(User, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)