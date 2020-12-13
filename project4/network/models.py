from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="User_Post")
    Contend=models.CharField(max_length=300)
    Date=models.DateTimeField(auto_now_add=True)
    like=models.ManyToManyField(User,blank=True,related_name="Post_likes")

    def __str__(self):
        return f"This is a Post created By {self.user.username}  and id:{self.pk}"

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="User_Profile")
    Follower=models.ManyToManyField(User,blank=True,related_name="User_Follower")
    Following=models.ManyToManyField(User,blank=True,related_name="User_Following")

    def __str__(self):
        return f"This is the profile of f{self.user.username} id:{self.id}"
