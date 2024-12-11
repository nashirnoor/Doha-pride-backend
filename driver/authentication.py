from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if user.password == password:
                user.set_password(password)
                user.save()
                return None
            
            if user.check_password(password):
                return user
            else:
                return None
        except UserModel.DoesNotExist:
            return None