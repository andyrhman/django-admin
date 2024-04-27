from rest_framework import serializers

from .models import Permission, User

class UserSerializer(serializers.ModelSerializer):
    # Adding a field for 'fullname' and map it to 'fullName' in the model
    fullname = serializers.CharField(source='fullName', max_length=255)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }    
          
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        # Convert email and username to lowercase
        email = validated_data.get('email', '').lower()
        username = validated_data.get('username', '').lower()
        
        # Update the dictionary with lowercase values
        validated_data['email'] = email
        validated_data['username'] = username

        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        
        
        