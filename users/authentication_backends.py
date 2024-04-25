from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# ? https://chat.openai.com/c/098a62b2-8c34-4d63-821d-73be066099b4
class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if '@' in username:
            # Handle email case-insensitively
            users = UserModel.objects.filter(email__iexact=username)
        else:
            # Handle username normally (case-sensitive)
            users = UserModel.objects.filter(username=username)

        for user in users:
            if user.check_password(password):
                return user
        return None
