from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import NewPostForm
from .models import User, NewPost, Profile, Follow


def index(request):
    posts = NewPost.objects.order_by("-date_posted").all()
    form = NewPostForm(request.POST)

    if request.POST == 'post':
        if form.is_valid():
            post_text = form.cleaned_data['post_text']
            new_post = NewPost(
                user_post=User.objects.get(pk=request.user.id),
                post_text=post_text
            )
            new_post.save()
        return render(request, "network/index.html")

    return render(request, "network/index.html", {
        "post_form": NewPostForm(),
        "posts": posts,
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


def new_post(request):
    if request.method == 'POST':
        post_text = request.POST['post_text']
        user_post = User.objects.get(pk=request.user.id)
        post = NewPost(post_text=post_text, user_post=user_post)
        post.save()
        return HttpResponseRedirect(reverse(index))


def user_profile(request, user_id):
    user_information = User.objects.get(pk=user_id)
    posts = NewPost.objects.filter(
        user_post=request.user.id).order_by("-date_posted").all()

    number_of_following = Follow.objects.filter(
        users_following=user_information)
    number_of_followers = Follow.objects.filter(
        user_followers=user_information)

    return render(request, 'network/user_profile.html', {
        "user_information": user_information,
        "posts": posts,
        "number_of_following": number_of_following,
        "number_of_followers": number_of_followers,
    })


def following(request, user_id):
    list_of_followings = Follow.objects.filter(users_following=user_id)

    return render(request, "network/following.html", {
        "list_of_followings": list_of_followings
    })


def follower(request, user_id):
    list_of_followers = Follow.objects.filter(user_followers=user_id)

    return render(request, "network/follower.html", {
        'list_of_followers': list_of_followers
    })


def likes_per_post(request, post_id):
    post_informations = NewPost.objects.filter(id=post_id)
    return render(request, "network/likes.html", {
        "post_informations": post_informations
    })


def like(request):
    return render(request, "network/index.html")
