from rest_framework import serializers
from .models import Profile, Post, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'twitter_name', 'profile_picture',
                  'birthday', 'email', 'location', 'date_created']
    name = serializers.StringRelatedField()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user_post', 'post_text',
                  'date_posted', 'number_of_likes']

    user_post = serializers.StringRelatedField()
