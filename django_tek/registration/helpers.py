import random
import string

import pytz
from django.conf import settings
from django.core.mail import send_mail
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


def get_password_reset_link(site_name, user):
	return '{}/reset_link'.format(site_name, user.pk)


def send_email_for_password_reset(user):
	site_name = 'localhost:8000'
	reset_link = get_password_reset_link(site_name, user)
	subject = 'Password Reset onTekkon'
	message = '''Dear {},\nYou have requested to reset your password in tekkon account. Please follow the link below to
reset password.\n{}'''.format(user.first_name, reset_link)
	from_email = settings.FROM_EMAIL
	recipient_list = [user.email]
	send_mail(subject, message, from_email, recipient_list)