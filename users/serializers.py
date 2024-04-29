from rest_framework import serializers

from .models import Permission, Role, User

class RoleRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return RoleSerializer(value).data
    def to_internal_value(self, data):
        try:
            return Role.objects.get(id=data)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Permission not found")

class UserSerializer(serializers.ModelSerializer):
    role = RoleRelatedField(queryset=Role.objects.all(), many=False)
    # Adding a field for 'fullname' and map it to 'fullName' in the model
    fullname = serializers.CharField(source='fullName', max_length=255)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'username', 'password', 'role']
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
    
    def update(self, instance, validated_data):
        # Convert email and username to lowercase if they are in the validated_data
        if 'email' in validated_data:
            validated_data['email'] = validated_data['email'].lower()
        if 'username' in validated_data:
            validated_data['username'] = validated_data['username'].lower()

        # Update other fields if included in the validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        """ Modify the output to remove 'password' field from the response. """
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret

    def validate(self, data):
        """ Customize validation based on the request method. """
        if self.context['request'].method in ['PUT', 'PATCH']:
            data.pop('password', None)  # Remove password from data if present
        return data
    
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        
class PermissionRelatedField(serializers.RelatedField):
    # ? Showing the permissions name and id, instead of number in get all roles
    def to_representation(self, value):
        return PermissionSerializer(value).data

    # ? For inserting the permission id data when creating role
    def to_internal_value(self, data):
        try:
            return Permission.objects.get(id=data)
        except Permission.DoesNotExist:
            raise serializers.ValidationError("Permission not found")
    
class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Role
        fields = "__all__"        
    def create(self, validated_data):
        permissions = validated_data.pop('permissions', None)
        instance = self.Meta.model(**validated_data)
        instance.save()
        instance.permissions.add(*permissions)
        instance.save()
        return instance
    
class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }    

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance    
    