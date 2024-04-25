import traceback
from decouple import config
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import exceptions, status

from users.authentication import generate_access_token

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

        # * Validation
        try:
            
            serializer.is_valid(raise_exception=True)
            
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except IntegrityError as e:
        
            if 'email' in str(e):
                return Response({"message": "This email already exists."}, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' in str(e):
                return Response({"message": "This username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Data integrity error."}, status=status.HTTP_400_BAD_REQUEST)
        
        except exceptions.ValidationError as e:
            # Generate a more user-friendly message that includes the field name
            errors = {key: value[0] for key, value in e.detail.items()}
            first_field = next(iter(errors))
            field_name = first_field.replace('_', ' ').capitalize()
            if 'required' in errors[first_field]:
                message = f"{field_name} is required."
            elif 'already exists' in errors[first_field]:
                message = f"{field_name.lower()} already exists."
            else:
                message = f"{field_name} error: {errors[first_field]}"
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        if config('DEBUG', cast=bool):
            traceback.print_exc()
        return Response({'message': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    data = request.data

    if 'email' in data:
        try:
            user = User.objects.get(email=data['email'].lower())
        except ObjectDoesNotExist:
            return Response({"message": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
    elif 'username' in data:
        try:
            user = User.objects.get(username=data['username'].lower())
        except ObjectDoesNotExist:
            return Response({"message": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
            
    password = request.data.get('password')
    remember_me = data.get('rememberMe', False)
    
    if user is None:
        return Response({"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
        return Response({"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
    response = Response()
    
    token = generate_access_token(user.id, remember_me)
    response.set_cookie(key='user_session', value=token, httponly=True)
    response.data = {
        'jwt': token
    }
    
    return response

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