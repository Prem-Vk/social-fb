from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    path("login/", views.UserLogin, name="login"),
    path("register", views.UserRegistration, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("user/<str:username>", views.home_page, name="home"),
    path("profile/<str:user>", views.profile_detail, name="profile"),
    path("search", views.SearchFriend, name="search"),
    path("friends", views.friends_page, name="friends"),
    path("comment/<int:pk>", views.post_comment, name="comment"),
]
