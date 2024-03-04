from django.contrib import admin
from.models import User, Like,Comment, Post,Friendship,FriendRequest

# Register your models here.
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
#admin.site.register(Profile)


