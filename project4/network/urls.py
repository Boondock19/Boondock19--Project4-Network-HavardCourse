
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Profile/<int:user_id>",views.ProfilePage,name="Profile"),
    path("Following", views.FollowingPage, name="FollowingPage"),
    path("EditPost/",views.EditPost),
    path("Liked/",views.Liked),
]
