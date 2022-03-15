from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=300)
    posting_time = models.DateTimeField(auto_now=False)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "users": self.users,
            "text": self.text,
            "posting_time": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.likes

        }

class Like(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post_id = models.IntegerField()

    def serialize(self):
        return {
            "id": self.id,
            "users": self.users,
            "post_id": self.post_id
        }

class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followers")
