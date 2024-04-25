from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullName', 'email', 'username', 'password'] # you can use '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }      