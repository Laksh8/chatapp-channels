from django.urls import path
from . import views


urlpatterns = [
    path("",views.index),
    path("user-notify/",views.user_notify),
    path("<str:room_name>/", views.one_to_one_chat, name="one-to-one-chat"),
]
