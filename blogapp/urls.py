
from django.urls import path
from blogapp import views

urlpatterns = [
    path("home/",views.home,name="home"),
    path("search/",views.search,name="search"),
    path("searchAPI/",views.searchAPI,name="searchAPI"),



    path("blog/<str:id>",views.blog,name="blog"),

    path("com/<str:id>",views.comment,name="comment"),

    path("reply/<str:id>",views.reply,name="reply"),
    path("like/<str:id>",views.like,name="like"),
    path("all_likes/<str:id>",views.all_likes,name="all_likes"),
    path("all_likes_comment/<str:id>",views.all_likes_comment,name="all_likes_comment"),


    path("unlike/<str:id>",views.unlike,name="unlike"),


    path("updatecomment/<str:id>",views.updatecomment,name="updatecomment"),
    path("comment/like/<str:id>",views.commentlike,name="commentlike"),
    path("comment/unlike/<str:id>",views.commentunlike,name="commentunlike"),
    path("updatereply/<str:id>",views.updatereply,name="updatereply"),
    
    path("reply/like/<str:id>",views.replylike,name="replylike"),
    path("reply/unlike/<str:id>",views.replyunlike,name="replyunlike"),

    path("deletecomment/<str:id>",views.deleteComment,name="deletecomment"),
    path("deletereply/<str:id>",views.deleteReply,name="deletereply"),



    path("createblog/",views.createblog,name="createblog"),
    path("about/",views.about,name="about"),
    path("notifications/",views.notifications,name="notifications"),
    path("notifications_ajax/",views.notifications_ajax,name="notifications_ajax"),

    path("notifications_length/",views.notifications_length,name="notifications_length"),
    path("followrequest_length/",views.followrequest_length,name="followrequest_length"),
    path("imageurl/",views.imageurl,name="imageurl"),
    
    path("followrequests/",views.followRequests,name="followrequests"),
    path("updateblog/<str:id>",views.updateblog,name="updateblog"),
    path("profile/<int:id>",views.profile,name="profile"),
    path("editprofile/<str:id>",views.editprofile,name="editprofile"),
      
]
