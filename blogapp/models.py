from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.db.models.fields import related
from django.urls import reverse
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.serializers import serialize
from tinymce.models import HTMLField
from django.utils import timezone

ACCOUNT_CHOICES = (
    ("public", "public"),
    ("private", "private")
)

NOTIFICATION_CHOICES = (
    ("comment", "comment"),
    ("reply", "reply"),
    ("likepost", "likepost"),
    ("likecomment", "likecomment"),
    ("likereply", "likereply")
)


class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    profileId = models.UUIDField(
            unique=True,
            primary_key=True,
            default=uuid4,
            help_text="Example: c8daa3ac-3dd0-44e9-ba2a-b0cbd1c8d8ae."
    )
    image=models.CharField(max_length=250,default="https://moonvillageassociation.org/wp-content/uploads/2018/06/default-profile-picture1.jpg")
    bio=models.CharField(max_length=250)
    accountType = models.CharField(
        max_length = 8,
        choices = ACCOUNT_CHOICES,
        default = 'public'
        )
    followers=models.ManyToManyField(User,related_name="following",blank=True)

    
    def __str__(self):
        return self.user.username
    
    def total_followers(self):
        return len(self.followers.all())

    def all_posts(self):
        return self.post_set.all()

    def posts_length(self):
        return len(self.post_set.all()
)
    
    def get_username(self):
        return self.user.username

    def total_following(self):
        l=0
        prof=Profile.objects.all()
        for pro in prof:
            if self.user in pro.followers.all():
                l=l+1

        return l

@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

class Post(models.Model):
    postId = models.UUIDField(
            unique=True,
            primary_key=True,
            default=uuid4,
            help_text="Example: c8daa3ac-3dd0-44e9-ba2a-b0cbd1c8d8ae."
    )
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,null=False)
    title=models.CharField(max_length=100)
    blog=HTMLField()
    imageURL=models.CharField(max_length=250)
    time = models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User,related_name='liking',blank=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.profile.user.username+" has posted "+self.title
    
    def get_absolute_url(self):
        return reverse("individual_post",kwargs={"uid":self.postId})
    
    def likeslength(self):
        return len(self.likes.all())

    def comments_length(self):
        return len(self.comments_set.all())




class Comments(models.Model):
    commentId = models.UUIDField(
            unique=True,
            primary_key=True,
            default=uuid4,
            help_text="Example: c8daa3ac-3dd0-44e9-ba2a-b0cbd1c8d8ae."
    )
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=False)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,null=False)
    comment=models.CharField(max_length=500)
    likes=models.ManyToManyField(User,related_name='commentliking',blank=True)
    created_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,blank=True,null=True)
    

    def __str__(self):
        return self.profile.user.username + " commented on "+str(self.post.postId)
    
    def replies(self):
        return self.replies_set.all();
    
    def replieslength(self):
        return len(self.replies_set.all())
    
    def likeslength(self):
        return len(self.likes.all())
    

    

@receiver(post_save, sender=Comments) 
def create_comment(sender, instance, created, **kwargs):
        if created:
            if instance.post.profile!=instance.profile:
                Notification.objects.create(acceptor=instance.post.profile,reactor=instance.profile,post=instance.post,notification_type="comment",created_at=timezone.now())



class Replies(models.Model):
    replyId = models.UUIDField(
            unique=True,
            primary_key=True,
            default=uuid4,
            help_text="Example: c8daa3ac-3dd0-44e9-ba2a-b0cbd1c8d8ae."
    )
    comment=models.ForeignKey(Comments,on_delete=models.CASCADE,null=False)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,null=False)
    reply=models.CharField(max_length=500)
    likes=models.ManyToManyField(User,related_name='replyliking',blank=True)
    
    class Meta:
        verbose_name="Replies"

    def __str__(self):
        return self.profile.user.username +" replied to "+str(self.comment.commentId)


@receiver(post_save, sender=Replies) 
def create_reply(sender, instance, created, **kwargs):
        if created:
            if instance.comment.profile!=instance.profile:
                Notification.objects.create(acceptor=instance.comment.profile,reactor=instance.profile,comment=instance.comment,notification_type="reply",created_at=timezone.now())


class Notification(models.Model):
    
    notificationId = models.UUIDField(
            unique=True,
            primary_key=True,
            default=uuid4,
            help_text="Example: c8daa3ac-3dd0-44e9-ba2a-b0cbd1c8d8ae."
    )

    reactor=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="reactor",null=True,blank=True)
    acceptor=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="acceptor",null=True,blank=True)
    notification_type=models.CharField(max_length=20,choices=NOTIFICATION_CHOICES)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    comment=models.ForeignKey(Comments,on_delete=models.CASCADE,null=True,blank=True)
    reply=models.ForeignKey(Replies,on_delete=models.CASCADE,null=True,blank=True)
    is_viewed=models.BooleanField(default=False,blank=True,null=True)
    created_at=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
         return self.reactor.user.username +" has "+self.acceptor.user.username+" "+str(self.notificationId)

class FollowRequest(models.Model):

    followrequestId = models.UUIDField(
            unique=True,
            primary_key=True,
            default=uuid4,
            help_text="Example: c8daa3ac-3dd0-44e9-ba2a-b0cbd1c8d8ae."
    )
    requestor=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="requestor",null=True,blank=True)
    request_acceptor=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="request_acceptor",null=True,blank=True)
    status=models.CharField(max_length=20,choices=(("pending","pending"),("accepted","accepted")),default="pending")
    
    def __str__(self):
        return self.requestor.user.username + " has requested to follow "




@receiver(post_save, sender=Notification) 
def create_notification(sender, instance, created, **kwargs):
        if created:
            channel_layer=get_channel_layer()
            noti=Notification.objects.filter(acceptor=instance.acceptor)
            noti_ser=serialize("json",noti)
            
            async_to_sync(channel_layer.group_send)(
                "notification%s" % instance.acceptor.user,{
                    'type':'noti_message',
                    'notification': noti_ser
                    
                }
            )

@receiver(post_save, sender=FollowRequest) 
def create_followrequest(sender, instance, created, **kwargs):
        if created:
            channel_layer=get_channel_layer()
            freq=FollowRequest.objects.filter(request_acceptor=instance.request_acceptor)
            print(freq)
            freq_ser=serialize("json",freq)
            async_to_sync(channel_layer.group_send)(
                "notification%s" % instance.request_acceptor.user.username,{
                    'type':'followrequest_message',
                    'followrequest': freq_ser
                    
                }
            )

