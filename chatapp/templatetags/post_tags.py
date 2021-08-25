from django import template
from chatapp.models import MessageReaction,Message
from blogapp.models import Profile
from django.utils.safestring import mark_safe

register=template.Library()

@register.simple_tag
def getMyReaction(messageId,user):
        message=Message.objects.get(messageId=messageId)
        prof=Profile.objects.get(user=user)
        msgRxn=MessageReaction.objects.filter(message=message).first()
        if msgRxn is not None:
                if msgRxn.reaction==True:
                        result='<i style="color:red" class="material-icons">favorite</i>'
                        return mark_safe(result)
                else:
                        return ""

        else:
                return ""
