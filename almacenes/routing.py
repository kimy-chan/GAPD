import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from almacenes.consumer import NotificacionConsumer  # Importa tus consumidores aquí

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almacenes.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    #'websocket': AuthMiddlewareStack(
     #   URLRouter([
            # Aquí añades las rutas para los WebSockets
      #      path('ws/notificaciones/', NotificacionConsumer.as_asgi()),
       # ])
    #),
})
