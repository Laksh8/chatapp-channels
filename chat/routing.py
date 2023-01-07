from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/group/(?P<group_name>\w+)/$", consumers.GroupChatConsumer.as_asgi()),
    re_path(r"ws/user/(?P<user_id>\w+)/$", consumers.UserChatConsumer.as_asgi()),
    re_path(r"ws/user-notify/$",consumers.PushUserConsumer.as_asgi()),
]