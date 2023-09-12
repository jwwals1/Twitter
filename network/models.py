from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user_post = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    post_text = models.CharField(max_length=240)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post_text} by {self.user_post}"


class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    twitter_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to="images/")
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=40)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s profile"


class Follow(models.Model):
    # User that follows other users
    users_following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following", null=True, blank=True)
    # Other users that follow user
    user_followers = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers", null=True, blank=True)

    def __str__(self):
        return f"{self.users_following} is following {self.user_followers}"


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} liked {self.post}"
