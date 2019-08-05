from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
	activation_key 	= models.CharField(max_length=50, blank=True)
	key_send_on		= models.DateTimeField(default=None, null=True)
	pass_reset_key 	= models.CharField(max_length=50, blank=True)
	pass_reset_on  	= models.DateTimeField(default=None, null=True)
