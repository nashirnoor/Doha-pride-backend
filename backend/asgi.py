"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# django.setup()  # Add this line to set up Django before importing other components
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack

# from django.core.asgi import get_asgi_application


# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     'http': django_asgi_app,
#     'websocket': AllowedHostsOriginValidator(
#         JWTAuthMiddlewareStack(
#             URLRouter(chat.routing.websocket_urlpatterns)
#         )
#     )
# })
