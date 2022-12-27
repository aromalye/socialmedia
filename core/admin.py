from atexit import register
from django.contrib import admin
from .models import Profile, Post, PostComments, PostLike, FollowProfile
# Register your models here.


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostComments)
admin.site.register(PostLike)
admin.site.register(FollowProfile)

