import jwt, datetime
from decouple import config
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_user_model

def generate_access_token(id, remember_me=False):
    if remember_me:
        # Set expiration to 1 year if "remember me" is checked
        exp_duration = datetime.timedelta(days=365)
    else:
        # Set expiration to 30 seconds if "remember me" is not checked
        exp_duration = datetime.timedelta(seconds=30)
    return jwt.encode({
        'user_id': str(id),  # Convert UUID to string
        'exp': datetime.datetime.now(datetime.timezone.utc) + exp_duration,
        'iat': datetime.datetime.now(datetime.timezone.utc)
    }, config('JWT_SECRET'), algorithm='HS256')
    
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('user_session')
        
        if not token:
            return None
        
        try:
            payload = jwt.decode(token, config('JWT_SECRET'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Unauthenticated')
        
        user = get_user_model().objects.filter(id=payload['user_id']).first()
        
        if user is None:
            raise exceptions.AuthenticationFailed('Unauthenticated')
         
        return (user, None)    
        