from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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

@csrf_exempt
def ProfilePage(request,user_id):
    
    userprofile=Profile.objects.get(user__id=user_id)
    userviewing=request.user
    UserviewingFollows=False
    userposts=Post.objects.filter(user__id=user_id).order_by("-Date")   
    userFollowers=userprofile.Follower
    userFollowing=userprofile.Following
    paginator=Paginator(userposts,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    
    
    if request.method== "POST":
        follows=request.POST.get('follows')
        if follows=="Follow":
            try: 
                ##Add request.user to the followers list of userprofile
                userFollowers.add(userviewing)
                userprofile.save()

                ##Add The user of userprofile to the following list of request.user
                userviewingprofile=Profile.objects.get(user__id=request.user.id)
                ## user of user profile:
                Owner_of_profile=User.objects.get(id=user_id)
                userviewingprofile.Following.add(Owner_of_profile)
                userviewingprofile.save()
                ##For the get request of the page
                UserviewingFollows=True
                Num_of_followers=userFollowers.count()
                return JsonResponse({'status': 201, 'follows': "Unfollow", "followerscount": Num_of_followers}, status=201)
            except:
                JsonResponse({},status=404) 
                return print(JsonResponse({},status=404))    
        else:
            ##Remove request.user of the followers list of userprofile
            userFollowers.remove(userviewing)
            userprofile.save()

            ##Remove The user of userprofile of the following list of request.user
            userviewingprofile=Profile.objects.get(user__id=request.user.id)
            ## user of user profile:
            Owner_of_profile=User.objects.get(id=user_id)
            userviewingprofile.Following.remove(Owner_of_profile)
            userviewingprofile.save()
            ##For the get request of the page
            UserviewingFollows=False
            Num_of_followers=userFollowers.count()
            return JsonResponse({'status': 201, 'follows': "Follow", "followerscount": Num_of_followers}, status=201)

    else:
        if userFollowers.filter(pk=userviewing.id).exists():
            UserviewingFollows=True

        context={"userprofile":userprofile.user,"followers":UserviewingFollows,"following":userFollowing,"followerscount":userFollowers.count(),
        "followingcount":userFollowing.count(),"page_obj":page_obj}
        return render(request,"network/ProfilePage.html",context)

      
def FollowingPage(request):
    userprofile=Profile.objects.get(user__id=request.user.id)
    userfollowing=userprofile.Following.all()
    posts=Post.objects.filter(user__in=userfollowing).order_by("-Date")   
    paginator=Paginator(posts,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    context={"page_obj":page_obj,"posts":posts}
    return render(request, "network/FollowingPage.html",context)
