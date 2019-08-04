from django.utils import timezone
from rest_framework import serializers

from registration.helpers import DateTimeSerializer, get_random_string
from registration.models import User


class UserSerializer(serializers.ModelSerializer):
	date_joined = DateTimeSerializer(format='%Y-%m-%d %H:%M', read_only=True, allow_null=True)
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'is_active', 'date_joined', 'is_staff', )
		
	def create(self, validated_data):
		random_string = get_random_string()
		validated_data['activation_key'] = random_string
		validated_data['key_send_on'] = timezone.now()
		validated_data['is_active'] = False
		return super().create(validated_data)