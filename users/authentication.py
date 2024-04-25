import jwt, datetime
from decouple import config

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