
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile_page/<int:id>", views.profile_page, name="profile_page"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow"),
    path("following_page", views.following_page, name="following_page"),

    #API Route
    path("posts/<int:post_id>", views.edit, name="edit"),
    path("likes", views.like, name="like"),
    path("unlike", views.unlike, name="unlike")
]
