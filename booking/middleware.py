# middleware.py
from threading import local
from django.contrib.auth.middleware import AuthenticationMiddleware

_thread_locals = local()

class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Make sure we have access to request.user
        if hasattr(request, 'user'):
            _thread_locals.user = request.user if request.user.is_authenticated else None
        else:
            _thread_locals.user = None
            
        response = self.get_response(request)
        return response