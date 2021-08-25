from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Product)
admin.site.register(models.MessageRoom)
admin.site.register(models.Message)
admin.site.register(models.MessageReaction)


