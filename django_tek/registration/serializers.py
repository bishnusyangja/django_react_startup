from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import serializers

from registration.helpers import DateTimeSerializer, get_random_string
from registration.models import User


class UserSerializer(serializers.ModelSerializer):
	date_joined = DateTimeSerializer(format='%Y-%m-%d %H:%M', read_only=True, allow_null=True)
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'is_active', 'date_joined', 'is_staff', )
		
	def set_password(self, user):
		passwd = get_random_string(size=10)
		user.set_password(passwd)
		user.save()
		return passwd
	
	def get_activation_link(self, site_name, user):
		return '{}/user/{}/activate/?activation_key={}'.format(site_name, user.pk, user.activation_key)
		
	def send_email(self, user):
		site_name = 'localhost:8000'
		activation_link = self.get_activation_link(site_name, user)
		passwd = self.set_password(user)
		subject = 'User Created in Tekkon'
		message = '''Dear {},\nYour account account has been created in Tekkon. Your Login credentials are\nusername:{}
\npassword:{}\nemail:{}\site:{}Click the link below to activate your account.\n{}'''.format(user.first_name, user.username,
				passwd, user.email, site_name, activation_link)
		from_email = settings.FROM_EMAIL
		recipient_list = [user.email]
		send_mail(subject, message, from_email, recipient_list)
		
	def create(self, validated_data):
		random_string = get_random_string()
		validated_data['activation_key'] = random_string
		validated_data['key_send_on'] = timezone.now()
		validated_data['is_active'] = False
		instance = super().create(validated_data)
		self.send_email(instance)
		return instance