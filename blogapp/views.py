from django.db.models.fields import NullBooleanField
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import  Profile,Post,Comments,Replies,Notification,FollowRequest
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import ast
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils import timezone
from chatapp.models import MessageRoom
from django.core.mail import send_mail
from django.conf import settings
from jose import jws
from django.contrib import messages



# Create your views here.
@login_required(login_url="/login/")
def home(request):
    posts=Post.objects.filter(profile__followers=request.user)|Post.objects.filter(profile=Profile.objects.get(user=request.user))
    p = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)  
    return render(request,"blogapp/home.html",{"posts":posts,"page_obj":page_obj})

@login_required(login_url="/login/")
def search(request):
    return render(request,"blogapp/search.html")

@login_required(login_url="/login/")
def searchAPI(request):
    data=json.loads(request.body)
    profile_list=[]
    users=User.objects.filter(username__icontains=data['username'])
    i=0;
    for user in users:
        new_mat=[]
        prof=Profile.objects.filter(user=user).first()
        new_mat.append(user.username)
        new_mat.append(prof.image)
        new_mat.append(user.id)
        profile_list.append(new_mat)

    return JsonResponse({"results":profile_list})


@login_required(login_url="/login/")
def notifications(request):
    profile=Profile.objects.get(user=request.user)
    notifications=Notification.objects.filter(acceptor=profile)
    return render(request,"blogapp/notifications.html",{"notifications":notifications})

@login_required(login_url="/login/")
def blog(request,id):

    likes=NullBooleanField;
    profile=Profile.objects.get(user=request.user)
    blog=Post.objects.filter(postId=id).first()

    if (request.user not in blog.profile.followers.all()) and blog.profile.user!=request.user and blog.profile.accountType=="private":
        return redirect("/blog/home")


    if request.user in blog.likes.all():
        like=True
    else:
        like=False
    comments=Comments.objects.filter(post=blog)

    if request.method=='POST'  and "deletebutton" in request.POST:
        post=Post.objects.get(postId=id)
        post.delete()
        return redirect(f'/blog/home')

    elif request.method=='POST'  and "deletecommentbutton" in request.POST:
        comment=Comments.objects.get(commentId=request.POST["commmentId"])
        comment.delete()
        return redirect(f'/blog/blog/{id}')
        
    else:
        print("Yugal")

    return render(request,"blogapp/blog.html",{"blog":blog,"like":like,"comments":comments,"length":len(comments)})

@login_required(login_url="/login/")
def createblog(request):
    profile=Profile.objects.get(user=request.user)
    if request.method=="POST":
        title=request.POST["title"]
        blog=request.POST["editor1"]
        imageURL=request.POST["imgURL"]
        print(imageURL)
        created_at=timezone.now()
        blog=Post.objects.create(profile=profile,blog=blog,title=title,imageURL=imageURL,created_at=created_at)
        blog.save()
        return redirect('/blog/home')
    return render(request,"blogapp/createblog.html")

@login_required(login_url="/login/")
def updateblog(request,id):
    post=Post.objects.get(postId=id)
    if post.profile.user==request.user:
        if request.method=="POST":
            title=request.POST["title"]
            blog=request.POST["editor1"]
            post.title=title
            post.blog=blog
            post.save()
            
            return redirect(f'/blog/blog/{post.postId}')
    
    return render(request,"blogapp/update.html",{"post":post})



def about(request):
    return render(request,"blogapp/about.html")

@login_required(login_url="/login/")
def followRequests(request):
    follow_requests=FollowRequest.objects.filter(request_acceptor=Profile.objects.get(user=request.user),status="pending")

    if request.method=="POST" and "accept" in request.POST:

        folreq=FollowRequest.objects.get(followrequestId=request.POST["requestId"])
        folreq.status="accepted";
        folreq.save()
        profile=Profile.objects.get(user=request.user)
        profile.followers.add(User.objects.get(id=request.POST["requestor"]))
        profile.save()

        return redirect('/blog/followrequests')

    
    if request.method=="POST" and "cancel" in request.POST:
        folreq=FollowRequest.objects.get(followrequestId=request.POST["requestId"])
        folreq.delete()

        return redirect('/blog/followrequests')
        


    return render(request,"blogapp/followrequests.html",{"follow_requests":follow_requests})

@login_required(login_url="/login/")
def profile(request,id):

    private=NullBooleanField
    user=User.objects.filter(id=id)[0]
    profile=Profile.objects.get(user=user)
    
    try:
        requests=FollowRequest.objects.filter(request_acceptor=profile,requestor=Profile.objects.get(user=request.user))[0]
    except:
        requests=[]
    
    
    if profile.accountType=="private" and request.user.id!=user.id:
        private=True
    else:
        private=False
    
    if request.method=="POST" and "following" in request.POST:
        profileId=request.POST.get("acceptor")
        request_acceptor=Profile.objects.filter(profileId=profileId).first()
        follow_request=FollowRequest.objects.create(requestor=Profile.objects.filter(user=request.user).first(),request_acceptor=request_acceptor)
        follow_request.save()

        return redirect(f'/blog/profile/{id}')

    if request.method=="POST" and "editprofile" in request.POST:
        user=User.objects.get(id=id)
        if user.id==request.user.id:
            user.first_name=request.POST.get("firstname")
            user.last_name=request.POST.get("lastname")
            user.username=request.POST.get("username")
            user.email=request.POST.get("email")
            profile.accountType=request.POST.get("accountType")
            user.save()
            profile.save();

            return redirect(f'/blog/profile/{profile.user.id}')

    if request.method=="POST" and "unfollow" in request.POST:
        profileId=request.POST.get("acceptor")
        request_acceptor=Profile.objects.get(profileId=profileId)
        follow_request=FollowRequest.objects.get(requestor=Profile.objects.get(user=request.user),request_acceptor=request_acceptor)
        follow_request.delete()
        request_acceptor.followers.remove(request.user)
        request_acceptor.save()
        
        return redirect(f'/blog/profile/{id}')
    
    if request.method=="POST" and "message" in request.POST:
        roomname=request.POST["roomname"]
        new_list=roomname.split(",")
        new_list1=new_list[0]+new_list[1]
        new_list2=new_list[1]+new_list[0]

        exists1=MessageRoom.objects.filter(roomName=new_list1) 
        exists2= MessageRoom.objects.filter(roomName=new_list2)
        print("The firstis ",exists1)
        print("the second is ",exists2 )
        
        if len(exists1)==1:
            return redirect(f'/chat/messages/{exists1[0].roomId}')
        elif len(exists2)==1:
            return redirect(f'/chat/messages/{exists2[0].roomId}')
           
        else:
            messageRoom=MessageRoom.objects.create(roomName=new_list1)
            profile1=Profile.objects.get(user=User.objects.get(username=new_list[0]))
            profile2=Profile.objects.get(user=User.objects.get(username=new_list[1]))
            messageRoom.user1=profile1
            messageRoom.user2=profile2
            messageRoom.save()

            return redirect(f'/chat/messages/{messageRoom.roomId}')

    return render(request,"blogapp/profile.html",{"profile":profile,"follow_requests":requests,"private":private})

@login_required(login_url="/login/")
def editprofile(request,id):
    
    profile=Profile.objects.get(profileId=id)
    user=User.objects.filter(id=profile.user.id)[0]

    if(user.id!=request.user.id):
        return redirect("/blog/home")

    if request.method=="POST":
        if user.id==request.user.id:
            user.first_name=request.POST.get("firstname")
            user.last_name=request.POST.get("lastname")
            user.username=request.POST.get("username")
            user.email=request.POST.get("email")
            profile.image=request.POST.get("img")
            profile.accountType=request.POST.get("accountType")
            user.save()
            profile.save();

            return redirect(f'/blog/profile/{profile.user.id}')

    return render(request,"blogapp/editprofile.html",{"profile":profile})

@login_required(login_url="/login/")
def like(request,id):

    post=Post.objects.get(postId=id)
    post.likes.add(request.user)
    post.save()
    if request.user != post.profile.user:
        Notification.objects.create(reactor=Profile.objects.get(user=request.user),
        acceptor=post.profile,notification_type="likepost",post=post,created_at=timezone.now()
        )

    if request.user in post.likes.all():
        liked=True
    else:
        liked=False

    return JsonResponse({'liked':liked})

@login_required(login_url="/login/")
def all_likes(request,id):
    post=Post.objects.get(postId=id)
    all=post.likes.all()
    print(all)
    all_likers=post.likes.all()
    ser_likes=serializers.serialize("json",all_likers,fields=("username"))
    return JsonResponse({'likes':json.dumps(ser_likes)})

@login_required(login_url="/login/")
def all_likes_comment(request,id):
    comment=Comments.objects.get(commentId=id)
    all=comment.likes.all()
    print(all)
    all_likers_comment=comment.likes.all()
    ser_likes=serializers.serialize("json",all_likers_comment,fields=("username"))
    return JsonResponse({'likes':json.dumps(ser_likes)})



@login_required(login_url="/login/")
def updatecomment(request,id):
    com=json.loads(request.body)

    comment=Comments.objects.filter(commentId=id).first()
    if request.user == comment.profile.user:
        comment.comment=com['comment']
        comment.save()
    return JsonResponse({'comment':comment.comment})

@login_required(login_url="/login/")
def updatereply(request,id):
    rep=json.loads(request.body)

    reply=Replies.objects.filter(replyId=id).first()
    if request.user == reply.profile.user:
        reply.reply=rep['reply']
        reply.save()
    return JsonResponse({'reply':reply.reply})



@login_required(login_url="/login/")
def unlike(request,id):
    # user=User.objects.get()
    post=Post.objects.get(postId=id)
    print(post)
    post.likes.remove(request.user)
    post.save()


    if request.user in post.likes.all():
        liked=True
    else:
        liked=False

    return JsonResponse({'liked':liked})

@login_required(login_url="/login/")
def commentlike(request,id):
    # user=User.objects.get()
    comment=Comments.objects.get(commentId=id)
    print(comment)
    comment.likes.add(request.user)
    comment.save()

    if request.user in comment.likes.all():
        liked=True
    else:
        liked=False

    return JsonResponse({'liked':liked})

@login_required(login_url="/login/")
def commentunlike(request,id):
    # user=User.objects.get()
    comment=Comments.objects.get(commentId=id)
    print(comment)
    comment.likes.remove(request.user)
    comment.save()

    if request.user in comment.likes.all():
        liked=True
    else:
        liked=False

    return JsonResponse({'liked':liked})

@login_required(login_url="/login/")
def deleteComment(request,id):
    comment=Comments.objects.get(commentId=id)
    comment.delete()
    return JsonResponse({'deletion':True})

@login_required(login_url="/login/")
def deleteReply(request,id):

    reply=Replies.objects.get(replyId=id)
    reply.delete()
    return JsonResponse({'deletion':True})

@login_required(login_url="/login/")
def replylike(request,id):
    # user=User.objects.get()
    reply=Replies.objects.get(replyId=id)
  
    reply.likes.add(request.user)
    reply.save()

    if request.user in reply.likes.all():
        liked=True
    else:
        liked=False

    return JsonResponse({'liked':liked})

@login_required(login_url="/login/")
def replyunlike(request,id):
    # user=User.objects.get()
    reply=Replies.objects.get(replyId=id)
    reply.likes.remove(request.user)
    reply.save()

    if request.user in reply.likes.all():
        liked=True
    else:
        liked=False

    return JsonResponse({'liked':liked})

@login_required(login_url="/login/")
def comment(request,id):
    comment=json.loads(request.body)
    print(comment)
    cmt=Comments.objects.create(post=Post.objects.get(postId=id),created_at=timezone.now(),profile=Profile.objects.get(user=request.user),comment=comment.get("comment"))
    cm=Comments.objects.filter(commentId=cmt.commentId)
    
    comment_id=str(Comments.objects.filter(commentId=cmt.commentId)[0].commentId)
    usr=User.objects.filter(id=request.user.id)
    user=serializers.serialize("json",usr)
    
    profile=serializers.serialize("json",Profile.objects.filter(user=request.user))
    serialized_comment=serializers.serialize("json",cm)

    return JsonResponse({'comment_id':comment_id,'comment':serialized_comment,'user':user,'profile':profile})


@login_required(login_url="/login/")
def reply(request,id):
    reply=json.loads(request.body)
    rpy=Replies.objects.create(comment=Comments.objects.get(commentId=id),reply=reply.get("reply"),profile=Profile.objects.get(user=request.user))
    rp=Replies.objects.filter(replyId=rpy.replyId)

    reply_id=str(Replies.objects.filter(replyId=rpy.replyId)[0].replyId)


    usr=User.objects.filter(id=request.user.id)
    user=serializers.serialize("json",usr)
    
    profile=serializers.serialize("json",Profile.objects.filter(user=request.user))
    serialized_reply=serializers.serialize("json",rp)

    return JsonResponse({'reply_id':reply_id,'reply':serialized_reply,'user':user,'profile':profile})

@login_required(login_url="/login/")
def notifications_ajax(request):
    noti_array=[]
    notifications=Notification.objects.filter(acceptor=Profile.objects.get(user=request.user)).order_by("-created_at")[:7]

    for noti in notifications:
        noti_1d={}
        noti_1d["image"]=noti.reactor.image
        noti_1d["username"]=noti.reactor.user.username
        noti_1d["postId"]=noti.post.postId
        if noti.comment:
            noti_1d["commentId"]=noti.comment.commentId
        if noti.reply:
            noti_1d["replyId"]=noti.reply.replyId
        
        print(noti.reactor.user.username)
        if noti.notification_type=="comment":
            noti_1d["notifications"]=str(noti.reactor.user.username)+" has commented on your post."
        elif noti.notification_type=="reply":
            noti_1d["notifications"]=noti.reactor.user.username+" has repied to your comment."
        elif noti.notification_type=="likepost":
            noti_1d["notifications"]=noti.reactor.user.username+" has liked your post."
        else:
            pass



        noti_1d["notification_type"]=noti.notification_type
        noti_1d["notificationId"]=noti.notificationId
        
        noti_array.append(noti_1d)

    return JsonResponse({'name':noti_array})


@login_required(login_url="/login/")
def notifications_length(request):
    print(request.user)
    noti=Notification.objects.filter(acceptor=Profile.objects.get(user=request.user))
    length=len(noti)
    return JsonResponse({"notifications_length":length})

@login_required(login_url="/login/")
def followrequest_length(request):
    freq=FollowRequest.objects.filter(request_acceptor=Profile.objects.get(user=request.user),status="pending")
    length=len(freq)
    return JsonResponse({"followrequest_length":length})

@login_required(login_url="/login/")
def imageurl(request):
    profile=Profile.objects.get(user=request.user)
    return JsonResponse({"image":profile.image})

def loginPage(request):
    error=""
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/blog/home/")
        else:
            error="Either wrong username or password"
    return render(request,"blogapp/login.html",{"error":error})

def forgotPassword(request):
        error=""
        token=""
        if request.user.is_authenticated:
            return redirect("/blog/home")
        if request.method=="POST":
            email=request.POST["email"]
            try:
                user=User.objects.get(email=email)
                try:
                    token = jws.sign({"email": user.email}, "mySecretKey", algorithm="HS256")
                    html_message=f'http://localhost:8000/resetpassword/{token}'

                    send_mail(
                        'LINK FOR PASSWORD RESET',
                        html_message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    messages.success(request, 'Email has been sent.Please cheack your email.')


                except:
                    messages.error(request, 'Something went wrong!!!!')
                    

            except:
                messages.error(request, 'User with this email doesnot exit!!')

        return render(request,"blogapp/forgotpassword.html",{"error":error})

def resetPassword(request,token):
    if request.user.is_authenticated:
            return redirect("/blog/home")
    if request.method=='POST':
            tok = jws.verify(token, 'mySecretKey', algorithms=['HS256'])
            json.loads(tok.decode("utf-8").replace("'",'"'))
            email=ast.literal_eval(tok.decode("utf-8"))['email']
            password=request.POST['password']
            user=User.objects.filter(email=email).first()
            user.set_password(password)
            user.save()

            return redirect("/login/")

    return render(request,"blogapp/resetpassword.html",{})



def registerPage(request):
    context={}
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password1"]
        email=request.POST["email"]
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        
        userexist=User.objects.filter(email=email)
        if len(userexist)!=0:
            context["error"]="User with this email already exists."
        else :
            user=User.objects.create_user(username=username,password=password,email=email,first_name=firstname,last_name=lastname)
            user.save()
            return redirect("/login/")

    return render(request,"blogapp/register.html",{"context":context})

@login_required(login_url="/login/")
def logoutP(request):
    
    logout(request)

    return redirect("/blog/home/")
