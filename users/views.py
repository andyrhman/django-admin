import traceback
from decouple import config
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import exceptions, status

from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
def register(request):
    try:
        data = request.data

        if 'password' not in data or 'password_confirm' not in data:
            return Response({"message": "Both password and password confirmation are required"}, status=status.HTTP_400_BAD_REQUEST)

        if data['password'] != data['password_confirm']:
            return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data)

        # * Validation check
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as e:
            # Generate a more user-friendly message that includes the field name
            errors = {key: value[0] for key, value in e.detail.items()}  # Create a dictionary of field: first_error
            first_field = next(iter(errors))  # Get the first field with an error
            field_name = first_field.replace('_', ' ').capitalize()  # Make field name more readable
            # Customize error messages for common cases
            if 'required' in errors[first_field]:
                message = f"{field_name} is required."
            elif 'already exists' in errors[first_field]:
                message = f"{field_name.lower()} already exists."
            else:
                message = f"{field_name} error: {errors[first_field]}"
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception:
        if config('DEBUG', cast=bool):
            traceback.print_exc()
        return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
@api_view(['GET'])
def users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except Exception:
        if config('DEBUG', cast=bool):
            traceback.print_exc()
        return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)