from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            print(f"Found user: {user.email}")
            if user.check_password(password):
                print("Password check passed")
                return user
            else:
                print("Password check failed")
                return None
        except UserModel.DoesNotExist:
            print(f"No user found with email: {email}")
            return None