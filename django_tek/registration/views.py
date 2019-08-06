import datetime
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from registration.helpers import get_random_string, send_email_for_password_reset
from registration.models import User
from registration.serializers import UserSerializer


class HomeView(TemplateView):
	# template_name = 'home.html'
	template_name = 'index.html'
	

class UserSerializerView(ModelViewSet):
	queryset = User.objects.none()
	serializer_class = UserSerializer
	# permission_classes = ()
	http_method_names = ('get', 'post', 'patch', )
	
	def get_queryset(self):
		if self.request.user.is_staff:
			User.objects.none()
		else:
			return User.objects.all()
		
	@action(methods=['GET'], detail=False)
	def activate(self, request, *args, **kwargs):
		validity = datetime.timedelta(days=3)
		params = self.request.query_params
		activation_key = params.get('activation_key', '')
		now_time = timezone.now()
		try:
			obj = User.objects.filter(activation_key=activation_key)
		except Exception as exc:
			dct = {'detail': 'No user found'}
		else:
			valid_till = obj.key_send_on + validity
			if now_time > valid_till:
				dct = {'detail': 'Link is expired.'}
			else:
				obj.is_active = True
				obj.save()
				dct = {'detail': '{} user with email {} activited successfully'.format(obj.username, obj.email)}
		return Response(dct, status=200)
	
	@action(methods=['POST'], detail=False)
	def forgot_password(self, request, *args, **kwargs):
		data = self.request.data
		email = data.get('email', '')
		try:
			obj = User.objects.get(email=email)
		except Exception as exc:
			dct = {'detail': 'No user found'}
		else:
			random_string = get_random_string()
			obj.pass_reset_key = random_string
			obj.pass_reset_on = timezone.now()
			obj.save()
			send_email_for_password_reset(obj)
			dct = {'detail': 'An email is sent to {} to reset password, follow the link in email'.format(obj.email)}
		return Response(dct, status=200)
	
	@action(methods=['POST'], detail=False)
	def reset_password(self, request, *args, **kwargs):
		validity = datetime.timedelta(days=3)
		params = self.request.data
		reset_key = params.get('reset_key', '')
		old_password = params.get('old_password', '')
		new_password = params.get('new_password', '')
		confirm_password = params.get('new_password', '')
		now_time = timezone.now()
		try:
			obj = User.objects.filter(pass_reset_key=reset_key)
		except Exception as exc:
			dct = {'detail': 'No user found'}
		else:
			valid_till = obj.key_send_on + validity
			if now_time > valid_till:
				dct = {'detail': 'Link is expired.'}
			else:
				if not new_password:
					dct = {'detail': 'new password is required'}
				elif not obj.check_password(old_password):
					dct = {'detail': 'old password did not match'}
				elif not new_password == confirm_password:
					dct = {'detail': 'password confirmation did not match.'}
				else:
					obj.set_password(new_password)
					obj.save()
					dct = {'detail': '{} user with email {} password change done successfully'.format(obj.username, obj.email)}
		return Response(dct, status=200)