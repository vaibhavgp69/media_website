from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import uuid #generates unique id 
from datetime import datetime
# Create your models here.

User = get_user_model()

class Profile(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        id_user = models.IntegerField()
        bio = models.TextField(blank=True)
        profileimg = models.ImageField(upload_to='profile_images', default='book-icon.png')
        location = models.CharField(max_length=100, blank=True)
        job =models.CharField(max_length=20, blank=True)
        
        
            
        def __str__(self):
            return self.user.username
  

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    no_of_dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
        
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    stats = models.CharField(max_length= 100,  null = True)
    
    def __str__(self):
        return self.username
    
class Follower(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.follower + " started to follow : " + self.user
    
class Comment(models.Model):
    poster = models.CharField(max_length=100)
    post_id = models.CharField(max_length=100)
    commenter = models.CharField(max_length=100)
    comment = models.CharField(max_length=500)
    
    def __str__(self):
        return self.commenter + " commented on :  " + self.poster + " ---> post_id = " + self.post_id
    