from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            
            # Verify the password is hashed
            if not user.password.startswith('pbkdf2_sha256$'):
                print("WARNING: Unhashed password detected!")
                print("this is unhasssheeddddddddd")
                return None
            
            if user.check_password(password):
                return user
            else:
                print("Password check failed")
                return None
        except UserModel.DoesNotExist:
            print(f"No user found with email: {email}")
            return None