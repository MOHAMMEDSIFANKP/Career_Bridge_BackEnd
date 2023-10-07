
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from .consumers import ChatConsumer

# application = ProtocolTypeRouter({
#     "websocket": URLRouter([
#         path("ws/chat/<int:id>/", ChatConsumer.as_asgi()),
#     ]),
# })

from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:id>/', ChatConsumer.as_asgi()),
]