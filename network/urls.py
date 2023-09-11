from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path("new_post", views.new_post, name="new_post"),
    path("following/<int:user_id>/", views.following, name="following"),
    path("follower/<int:user_id>/", views.follower, name="follower"),
    path("likes/<int:post_id>/", views.likes_per_post, name="likes"),
]
