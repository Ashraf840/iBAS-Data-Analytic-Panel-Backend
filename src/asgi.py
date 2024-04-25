"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
django.setup()

import final_dataset_operations.routing as fdo_r
import addToDataset.routing as atd_r

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        # Just HTTP for now. (We can add other protocols later.)
        "http": django_asgi_app,
        'websocket': AuthMiddlewareStack(
            URLRouter(
                fdo_r.websocket_urlpatterns +
                atd_r.websocket_urlpatterns
            ),
        ),
    }
)