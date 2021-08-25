from django.db import models
from tinymce.models import HTMLField
from uuid import uuid4
from django.utils import timezone
from blogapp.models import Profile
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.serializers import serialize
from django import template
# Create your models here.
REACTION_OPTIONS=(
    ("like","like"),
    ("love","love"),
    ("sad","sad"),
    ("haha","haha")
)


class Product(models.Model):
    name=models.CharField(max_length=400)
    content = HTMLField()

class MessageRoom(models.Model):
    roomId=models.UUIDField(
            unique=True,
            primary_key=True,
            default=uuid4,
            help_text="Example: c8daa3ac-3dd0-44e9-ba2a-b0cbd1c8d8ae."
    )
    roomName=models.CharField(max_length=500)
    user1=models.ForeignKey(Profile,related_name="user1",on_delete=models.CASCADE,null=True,blank=True)
    user2=models.ForeignKey(Profile,related_name="user2",on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.roomName
    
    def latestMessage(self):
        lastMessage=self.message_set.filter(room=self).order_by("-sent_at")[0]
        return lastMessage.message
    

        

class Message(models.Model):
    messageId=models.UUIDField(
            unique=True,
            primary_key=True,
            default=uuid4,
            help_text="Example: c8daa3ac-3dd0-44e9-ba2a-b0cbd1c8d8ae."
    )
    room=models.ForeignKey(MessageRoom,on_delete=models.CASCADE)
    messeger=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    message=models.CharField(max_length=1000)
    sent_at=models.DateTimeField(default=timezone.now())
    
    
    def __str__(self):
        return self.message

    # def MyReaction(self,user):
    #     prof=Profile.objects.get(user=user)
    #     return self.messagereaction_set.get(message=self,reactor=prof).reaction
    
    # def totalReactions(self):
    #     return len(MessageReaction.objects.filter(message=self))
    
    

class MessageReaction(models.Model):
    messageReactionId=models.UUIDField(
            unique=True,
            primary_key=True,
            default=uuid4,
            help_text="Example: c8daa3ac-3dd0-44e9-ba2a-b0cbd1c8d8ae."
    )
    message=models.ForeignKey(Message,on_delete=models.CASCADE)
    reactor=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    reaction=models.BooleanField(default=True)
    
    def __str__(self):
        return self.message.message
    
    
    


# @receiver(post_save, sender=Message) 
# def create_message(sender, instance, created, **kwargs):
#         if created:
#             roomId=instance.room.roomId
#             async_to_sync(channel_layer.group_send)(
#                 "room_%s" % instance.room.roomId,{
#                     'type':'noti_message',
#                     'message': instance.message
                    
#                 }
#             )
            