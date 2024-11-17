from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        print("callllllll")
        try:
            user = UserModel.objects.get(email=email)
            print(user,"this is user")
            if user.check_password(password):
                print(user,"inside check")
                return user
        except UserModel.DoesNotExist:
            return None
        return None