from django.db import models
from django.contrib.auth.models import User

class WashingRecord(models.Model):
	country 		= models.CharField(max_length=50, blank=False)
	city 			= models.CharField(max_length=50, blank=False)
	time_stamp 		= models.DateTimeField(auto_now_add=False, blank=False)

	def __str__(self):
		return "time"