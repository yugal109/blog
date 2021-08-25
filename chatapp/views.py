# chat/views.py
from django.shortcuts import redirect, render
from .models import Product
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import MessageRoom,Message
from blogapp.models import Profile

@login_required(login_url="/login/")
def inbox(request):
    messageRooms=MessageRoom.objects.filter(user1=Profile.objects.get(user=request.user)) | MessageRoom.objects.filter(user2=Profile.objects.get(user=request.user))
    if len(messageRooms)==0:
        messageRooms=[]
        
    return render(request,"chatapp/inbox.html",{"inbox_list":messageRooms})

@login_required(login_url="/login/")
def messagesRoom(request,id):
    msgRoom=MessageRoom.objects.get(roomId=id)
    
    if msgRoom.user1==Profile.objects.get(user=request.user):
        frnd=msgRoom.user2
    elif msgRoom.user2==Profile.objects.get(user=request.user):
        frnd=msgRoom.user1
    else:
        return redirect("/chat/inbox")

    messages=Message.objects.filter(room=id)
    image=Profile.objects.get(user=request.user).image
    
    return render(request,"chatapp/chat.html",{"messages":messages,"image":image,"friend":frnd})