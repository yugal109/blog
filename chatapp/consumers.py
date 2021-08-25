# chat/consumers.py
from chatapp.views import messagesRoom
from chatapp.models import Message, MessageRoom,MessageReaction
import json
from os import access
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from blogapp.models import Profile,Notification,FollowRequest
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from blogapp.models import Notification
from django.utils import timezone

class NotificationConsumer(WebsocketConsumer):
    USER=""
    def connect(self):
        self.notification_group_name = 'notification%s' % self.scope['user']
        self.USER=self.scope['user']
       
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name ,
            self.channel_name
        )

        self.accept()

    def disconnect(self,close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name ,
            self.channel_name
        )
    
    def receive(self, text_data):
        # Send message to room group
        prof=Profile.objects.get(user=self.USER)
        noti=Notification.objects.filter(acceptor=prof)
        noti_ser=serialize("json",noti)
        freq=FollowRequest.objects.filter(request_acceptor=prof)
        freq_ser=serialize("json",freq)
        
        async_to_sync(self.channel_layer.group_send)(
            self.notification_group_name ,
            {   
                'type':'noti_message',
                'notification': noti_ser
            }
        )

        async_to_sync(self.channel_layer.group_send)(
            self.notification_group_name ,
            {   
                'type':'followrequest_message',
                'followrequest': freq_ser
            }
        )

    def noti_message(self, event):  
        self.send(text_data=json.dumps({'notifications':event['notification']}))
    
    def followrequest_message(self, event):  
        print(event['followrequest'])
        self.send(json.dumps({'followrequest':event['followrequest']}))


class FollowRequestConsumer(WebsocketConsumer):
    USER=""
    def connect(self):
        self.follow_request_group_name = 'followrequest%s' % self.scope['user']
        self.USER=self.scope['user']
        print("The request group name is ",self.follow_request_group_name )
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.follow_request_group_name ,
            self.channel_name
        )

        self.accept()

    def disconnect(self,close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.follow_request_group_name ,
            self.channel_name
        )
    
    def receive(self, text_data):
        # Send message to room group
        prof=Profile.objects.get(user=self.USER)
        freq=FollowRequest.objects.filter(request_acceptor=prof)
        freq_ser=serialize("json",freq)
        
        async_to_sync(self.channel_layer.group_send)(
            self.follow_request_group_name ,
            {   
                'type':'followrequest_message',
                'followrequest': freq_ser
            }
        )

    def followrequest_message(self, event):  
        self.send(text_data=json.dumps({'followrequest':event['followrequest']}))


class ChatConsumer(WebsocketConsumer):
   
    roomid=""
    def connect(self):
        roomId=self.scope['url_route']['kwargs']['roomId']
        self.room_id="room_%s" %roomId
        self.roomid=roomId
        async_to_sync(self.channel_layer.group_add)(
            self.room_id,
            self.channel_name
        )
        
        self.accept()
    
    def receive(self, text_data):

        json_data=json.loads(text_data)
        
        if "messageId" in json_data and "reaction_type" in json_data:
            messageId=json.loads(text_data)['messageId']
            reaction_type=json.loads(text_data)['reaction_type']
            message=Message.objects.get(messageId=messageId)
            existReaction=MessageReaction.objects.filter(message=message,reactor=Profile.objects.get(user=self.scope['user'])).first()
            if existReaction:
                existReaction.reaction=not existReaction.reaction
                existReaction.save()
                msgId=str(existReaction.message.messageId)

                async_to_sync(self.channel_layer.group_send)(
                    self.room_id,
                    {   
                        'type':'react_message',
                        'reaction': existReaction.reaction,
                        'messageId':msgId
                    }
                )
            else: 
                 
                messageReaction=MessageReaction.objects.create(message=message,reactor=Profile.objects.get(user=self.scope['user']))
                msgId=str(messageReaction.message.messageId)
                
                async_to_sync(self.channel_layer.group_send)(
                    self.room_id,
                    {   
                        'type':'react_message',
                        'reaction': messageReaction.reaction,
                        'messageId':msgId  
                    }
                )

    
        if "message" in json_data:
            message=json.loads(text_data)['message']
            messageRoom=MessageRoom.objects.get(roomId=self.roomid)
            msg=Message.objects.create(room=messageRoom,
            messeger=Profile.objects.get(user=self.scope['user']),
            message=message,
            sent_at=timezone.now())
            messageId=str(msg.messageId)

            async_to_sync(self.channel_layer.group_send)(
                self.room_id ,
                {   
                    'type':'send_message',
                    'message': message,
                    'userid':msg.messeger.user.id,
                    "messageId":messageId,
                    "imageurl":msg.messeger.image
                }
            )
        
    
    def send_message(self,event):
        self.send(json.dumps({"message":event['message'],"userid":event['userid'],"messageId":event['messageId'],"imageurl":event['imageurl']}))
    

    def react_message(self,event):
        self.send(json.dumps({"reaction":event['reaction'],"messageId":event['messageId']}))


    def disconnect(self, code):
         # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_id ,
            self.channel_name
        )      
                    
        

