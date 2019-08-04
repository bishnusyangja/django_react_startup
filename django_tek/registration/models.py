from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
	activation_key 	= models.CharField(max_length=50)
	key_send_on		= models.DateTimeField(default=None, null=True)
