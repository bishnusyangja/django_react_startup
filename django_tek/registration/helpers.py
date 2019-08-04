import random
import string

import pytz
from django.conf import settings
from rest_framework import serializers, permissions


def get_np_time(value):
	np = pytz.timezone(settings.TIME_ZONE)
	value = value.astimezone(np)
	return value


class DateTimeSerializer(serializers.DateTimeField):

	def to_representation(self, value):
		value = get_np_time(value)
		date = super(DateTimeSerializer, self).to_representation(value)
		# print 'date :', date
		# format date here or just by pass above super call
		return date


class LoginPermissionPermission(permissions.BasePermission):
	"""
	Permission class for Login Permission
	 """
	
	def has_permission(self, request, view):
		"""
		permission for listView
		:param request:
		:param view:
		:return:
		"""
		return True
	
	def has_object_permission(self, request, view, obj):
		# check if account is owner
		return request.user
	
	
def get_random_string(size=30, chars=string.ascii_letters+string.digits):
	return ''.join(random.choice(chars) for x in range(size))