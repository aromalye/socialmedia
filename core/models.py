from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


user = get_user_model()
# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='blank-profile-picture.png', upload_to='profile_img')
    location = models.CharField(blank=True, max_length=100)
    bio = models.TextField(blank=True, max_length=300)
    follower_count = models.IntegerField(default=0, blank=True)
    following_count = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return self.user.username

    def full_name(self):
        return (self.user.first_name) + " " + (self.user.last_name)


class FollowProfile(models.Model):
    user = models.CharField(max_length=100) #user
    following_user = models.CharField(max_length=100) #friend

    def __str__(self):
        return self.following_user


class Post(models.Model):
    post = models.ImageField()
    caption = models.CharField(blank=True, max_length=200)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.IntegerField(default=0, blank=True)

    def __int__(self):
        return self.id
 

class PostComments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
