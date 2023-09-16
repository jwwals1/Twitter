from django.urls import path
from . import views

urlpatterns = [
    path("/<int:post_id>/", views.index, name="index"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('user_profile/<int:post_id>/', views.user_profile, name='user_profile'),
    path("new_post", views.new_post, name="new_post"),
    path("follower/<int:user_id>/", views.follower, name="follower"),
    path("following/<int:user_id>/", views.following, name="following"),
    path("add_like/<int:post_id>/", views.add_like, name="add_like"),
    path("follow<int:user_id>", views.follow, name='follow'),
    path("likepage<int:post_id>", views.like_page, name="likepage"),
    path("add_like_user_page/<int:user_id>/<int:post_id>/",
         views.add_like_user_page, name="add_like_user_page"),
    path("add_like_user_page/<int:post_id>/",
         views.add_like_user_page, name="add_like_user_page"),
    path("search", views.search, name="search"),
    path("followingpost", views.following_post, name="followingpost"),
    path("add_like_following_page/<int:post_id>/",
         views.add_like_following_page, name="add_like_following_page"),
]
