from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import *


def index(request):
    
    if request.method== "POST":
        userPosting=request.user
        NewPost=Post()
        NewPost.user=userPosting
        NewPost.Contend=request.POST["NewPost"]
        NewPost.save()
        return HttpResponseRedirect(reverse("index"))
    else: 
        posts=Post.objects.all().order_by("-Date")   
        paginator=Paginator(posts,10)
        page_number=request.GET.get("page")
        page_obj=paginator.get_page(page_number)
        context={"page_obj":page_obj,"posts":posts}
        return render(request, "network/index.html",context)


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
            Newuser = User.objects.create_user(username, email, password)
            Newuser.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        #Creates a profile for the new user
        NewProfile=Profile()
        NewProfile.user=Newuser
        NewProfile.save()
        login(request, Newuser)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def AddPost(request):
    
    if request.method== "POST":
        userPosting=User.username
        NewPost=Post()
        NewPost.user=userPosting
        NewPost.contend=request.POST["NewPost"]
        NewPost.save()
        return HttpResponseRedirect(reverse("index"))

    else :
        posts=Post.objects.all()
        return render(request,"network/index.hmtl")

def ProfilePage(request,user_id):
    userprofile=Profile.objects.get(user__id=user_id)
    userposts=Post.objects.filter(user__id=user_id).order_by("-Date")   
    userFollowers=userprofile.Follower.count()
    userFollowing=userprofile.Following.count()
    paginator=Paginator(userposts,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    context={"userprofile":userprofile.user,"followers":userFollowers,"following":userFollowing,"page_obj":page_obj}
    return render(request,"network/ProfilePage.html",context)
