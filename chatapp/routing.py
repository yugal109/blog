# chat/routing.py
from channels import consumer
from django.urls import path
from . import consumers

ws_urlpatterns = [
    path(r'ws/notifications/',consumers.NotificationConsumer.as_asgi()),
    path(r'ws/followrequest/',consumers.FollowRequestConsumer.as_asgi()),
    path("ws/chat/<str:roomId>",consumers.ChatConsumer.as_asgi())

]