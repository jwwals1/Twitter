from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import NewPostForm
from .models import User, Post, Profile, Follow, Like
from itertools import chain
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.all().order_by("-date_posted")
    form = NewPostForm(request.POST)
    alllikes = Like.objects.all()

    if request.POST == 'post':
        if form.is_valid():
            post_text = form.cleaned_data['post_text']
            new_post = Post(
                user_post=User.objects.get(pk=request.user.id),
                post_text=post_text
            )
            new_post.save()
        return render(request, "network/index.html")

    return render(request, "network/index.html", {
        "post_form": NewPostForm(),
        "posts": posts,
        "alllikes": alllikes,
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
        post = Post(post_text=post_text, user_post=user_post)
        post.save()
        return HttpResponseRedirect(reverse(index))


def user_profile(request, user_id):
    user_information = User.objects.get(pk=user_id)
    posts = Post.objects.filter(
        user_post=user_information).order_by("-date_posted").all()

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


def add_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(pk=request.user.id)
    like_value = Like.objects.filter(post_id=post_id, user=user).first()
    username = request.user

    if like_value == None:
        newlike = Like(user=username, post=post)
        post.number_of_likes = post.number_of_likes + 1
        newlike.save()
        post.save()
        return HttpResponseRedirect(reverse(index))
    else:
        like_value.delete()
        post.number_of_likes = post.number_of_likes - 1
        post.save()
        return HttpResponseRedirect(reverse(index))


def add_like_user_page(request, post_id, user_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(pk=request.user.id)
    like_value = Like.objects.filter(post_id=post_id, user=user).first()
    username = request.user

    if like_value == None:
        newlike = Like(user=username, post=post)
        post.number_of_likes = post.number_of_likes + 1
        newlike.save()
        post.save()
        return HttpResponseRedirect(reverse("user_profile", args=[user_id]))
    else:
        like_value.delete()
        post.number_of_likes = post.number_of_likes - 1
        post.save()
        return HttpResponseRedirect(reverse("user_profile", args=[user_id]))


def add_like_following_page(request, post_id, user_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(pk=request.user.id)
    like_value = Like.objects.filter(post_id=post_id, user=user).first()
    username = request.user

    if like_value == None:
        newlike = Like(user=username, post=post)
        post.number_of_likes = post.number_of_likes + 1
        newlike.save()
        post.save()
        return HttpResponseRedirect(reverse(following_post))
    else:
        like_value.delete()
        post.number_of_likes = post.number_of_likes - 1
        post.save()
        return HttpResponseRedirect(reverse(following_post))


def follow(request, user_id):
    if request.method == "POST":
        users_following = request.user
        user_followers = User.objects.get(pk=user_id)

        if Follow.objects.filter(users_following=users_following, user_followers=user_followers).first():
            delete_follow = Follow.objects.get(
                users_following=users_following, user_followers=user_followers)
            delete_follow.delete()
            return HttpResponseRedirect(reverse("user_profile", args=[user_id]))
        else:
            add_follow = Follow.objects.create(
                users_following=users_following, user_followers=user_followers)
            add_follow.save()
            return HttpResponseRedirect(reverse("user_profile", args=[user_id]))


def like_page(request, post_id):
    list_of_likes = Like.objects.filter(post=post_id)
    return render(request, 'network/likepage.html', {
        'list_of_likes': list_of_likes
    })


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        users = User.objects.filter(username__contains=searched)

        return render(request, "network/search.html",
                      {'searched': searched,
                       'users': users})

    else:
        return render(request, "network/search.html", {})


def following_post(request):
    current_user = User.objects.get(pk=request.user.id)
    following_accounts = Follow.objects.filter(users_following=current_user)
    all_post = Post.objects.all().order_by('id').reverse()

    following_posts = []

    for post in all_post:
        for account in following_accounts:
            if account.user_followers == post.user_post:
                following_posts.append(post)

    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page')
    posts_on_page = paginator.get_page(page_number)

    return render(request, "network/followingpost.html", {
        'posts_on_page': posts_on_page
    })
