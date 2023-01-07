from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
    return render(request, "chat/index.html")

def one_to_one_chat(request, room_name):
    return render(request, "chat/one-to-one-chat.html", {"room_name": room_name})


def user_notify(request):
    users = User.objects.all()
    return render(request,"chat/user-notify.html",{"users":users})