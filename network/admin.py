from django.contrib import admin
from .models import User, Followers, Post

# Register your models here.
@admin.register(Followers)
class FollowersAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following']

@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ['users', 'text', 'posting_time', 'likes']
