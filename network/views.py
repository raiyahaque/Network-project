import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import datetime


from .models import User, Post, Followers, Like

def get_user(request):
    username = request.user.username
    user = User.objects.get(username=username)
    return user

def index(request):
    liked_posts = []
    # Get all posts with the most recent one first
    posts = Post.objects.all().order_by('posting_time').reverse()
    # Limit ten posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        user = get_user(request)
        # Get all of the user's likes
        user_likes = Like.objects.filter(users=user)
        for like in user_likes:
            liked_posts.append(like.post_id)
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='/login')
def new_post(request):
    if request.method == "POST":
        text = request.POST.get("text")
        user = get_user(request)
        # Create new post
        newPost = Post(users=user, text=text, posting_time=datetime.datetime.now())
        newPost.save()

    return HttpResponseRedirect(reverse("index"))


def profile_page(request, id):
    # Get user object
    user_profile = User.objects.get(pk=id)
    followers = None
    if request.user.is_authenticated:
        user = get_user(request)
        try:
            # See if user follows profile
            followers = Followers.objects.get(follower=user, following=user_profile)
        except Followers.DoesNotExist:
            # User does not follow profile
            followers = None
    # Check how many followers the profile has
    user_followers = Followers.objects.filter(following=user_profile).count()
    # Check how many users the profile follows
    user_following = Followers.objects.filter(follower=user_profile).count()
    posts = Post.objects.filter(users=user_profile).order_by('posting_time').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile_page.html", {
        "user_profile": user_profile,
        "followers": followers,
        "user_followers": user_followers,
        "user_following": user_following,
        "page_obj": page_obj
    })

@login_required(login_url='/login')
def follow(request, id):
    user = get_user(request)
    user_profile = User.objects.get(pk=id)
    follower = get_user(request)
    following = User.objects.get(pk=id)
    # Create new follower if user follows profile
    new_follower = Followers(follower=follower, following=following)
    new_follower.save()
    try:
        followers = Followers.objects.get(follower=user, following=user_profile)
    except Followers.DoesNotExist:
        followers = None
    user_followers = Followers.objects.filter(following=user_profile).count()
    user_following = Followers.objects.filter(follower=user_profile).count()
    posts = Post.objects.filter(users=user_profile).order_by('posting_time').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile_page.html", {
        "user_profile": user_profile,
        "followers": followers,
        "user_followers": user_followers,
        "user_following": user_following,
        "page_obj": page_obj,
        "user": user


    })

@login_required(login_url='/login')
def unfollow(request, id):
    user_profile = User.objects.get(pk=id)
    user = get_user(request)
    # Delete follower object if user unfollows profile
    removed = Followers.objects.get(follower=user, following=user_profile)
    removed.delete()
    try:
        followers = Followers.objects.get(follower=user, following=user_profile)
    except Followers.DoesNotExist:
        followers = None
    user_followers = Followers.objects.filter(following=user_profile).count()
    user_following = Followers.objects.filter(follower=user_profile).count()
    posts = Post.objects.filter(users=user_profile).order_by('posting_time').reverse()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/profile_page.html", {
        "user_profile": user_profile,
        "followers": followers,
        "user_followers": user_followers,
        "user_following": user_following,
        "page_obj": page_obj,
        "user": user


    })

@login_required(login_url='/login')
def following_page(request):
    user = get_user(request)
    posts_list = []
    users_list = []
    # Get every post
    posts = Post.objects.all().order_by('posting_time').reverse()
    # Get all follower objects where user is the follower
    user_following = Followers.objects.filter(follower=user)
    for users in user_following:
        # Append all of the profiles the user follows in a list
        users_list.append(users.following)

    for post in posts:
        # Check if user who created the post is followed by user who is signed in
        if post.users in users_list:
            posts_list.append(post)

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked_posts = []
    user_likes = Like.objects.filter(users=user)
    for like in user_likes:
        liked_posts.append(like.post_id)

    return render(request, "network/following_page.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })

@csrf_exempt
@login_required(login_url='/login')
def edit(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == 'GET':
        return JsonResponse(post.serialize())
    elif request.method == 'POST':
        data = json.loads(request.body)
        if data.get("text") != None:
            # Replace text with new text
            post.text = data["text"]
            # Update posting time
            post.posting_time = datetime.datetime.now()
        else:
            return JsonResponse({
                "error": "Text required."
                }, status=400)

    post.save()
    return JsonResponse({"message": "Text updated successfully."}, status=201)

@csrf_exempt
@login_required(login_url='/login')
def like(request):
    data = json.loads(request.body)
    if data.get("post_id") != None:
        user = get_user(request)
        # Create like for that post
        like = Like(users=user, post_id=data["post_id"])
        like.save()
        try:
            post = Post.objects.get(pk=data["post_id"])
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        # Increase post's likes by 1
        post.likes += 1
        post.save()
        return JsonResponse({"message": "Liked successfully."}, status=201)

    else:
        return JsonResponse({
            "error": "Could not like."
        }, status=400)

@csrf_exempt
@login_required(login_url='/login')
def unlike(request):
    data = json.loads(request.body)
    if data.get("post_id") != None:
        user = get_user(request)
        # Remove like from that post
        like = Like.objects.get(users=user, post_id=data["post_id"])
        like.delete()
        try:
            post = Post.objects.get(pk=data["post_id"])
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        # Decrease post's likes by 1
        post.likes -= 1
        post.save()
        return JsonResponse({"message": "Unliked successfully."}, status=201)
    else:
        return JsonResponse({
            "error": "Could not unlike."
        }, status=400)
