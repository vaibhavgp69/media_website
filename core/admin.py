from django.contrib import admin
from .models import Profile, Post ,LikePost, Follower, Comment

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Follower)
admin.site.register(Comment)

