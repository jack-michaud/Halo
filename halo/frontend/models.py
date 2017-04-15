from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	databases = models.ManyToManyField('Database', through='ProfileAccessDatabase')

class Database(models.Model):
	user = models.TextField(null=False)
	password = models.TextField(null=False)
	name = models.TextField(null=False)
	host_and_port = models.TextField(null=True, default="localhost:5672")

class ProfileAccessDatabase(models.Model):
	profile = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
	database = models.ForeignKey('Database', on_delete=models.DO_NOTHING)

class Query(models.Model):
	created_ts = models.DateTimeField(auto_now=True)

	created_by = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
	database = models.ForeignKey('Database', on_delete=models.DO_NOTHING)
	querystring = models.TextField(null=False)

class Graph(models.Model):
	query = models.ForeignKey('Query', on_delete=models.CASCADE)
	created_ts = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
	x = models.TextField(null=False)
	y = models.TextField(null=False)
