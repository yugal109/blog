from django.contrib import admin
from blogapp import models
# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Comments)
admin.site.register(models.Replies)
admin.site.register(models.Notification)
admin.site.register(models.FollowRequest)


