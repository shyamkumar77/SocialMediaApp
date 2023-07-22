from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save  

from random import sample

# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    # requst.user --> gives user object
    # related_name="profile"
    # request.user.profile--> goes to Userprofile Model. so, request.user.profile.profile_pic --> gives loggined user profile pic
    profile_pic=models.ImageField(upload_to="profilepics",blank=True,default="/profilepics/default.jpg")
    bio=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=200,null=True)
    dob=models.DateTimeField(null=True)
    following=models.ManyToManyField("self",related_name="followed_by",symmetrical=False) #a user can follow many other Userprofiles, self: means the relation is given to this Userprofile model itself
    created_date=models.DateTimeField(auto_now_add=True)
    cover_pic=models.ImageField(upload_to="coverpic",blank=True,default="/profilepics/cover.jpg")

    def __str__(self):
        return self.user.username 
    

  
    
    # for friend request suggestion using custom method
    @property
    def friend_requests(self):
        all_profiles=UserProfile.objects.all().exclude(user=self.user)
        following_profiles=self.following.all()
        suggestions=set(all_profiles) - set(following_profiles)
        # only need 2 suggestions at a time
        if len(suggestions)>2:
            return sample(list(suggestions),2)
        
        return suggestions
       
    


class Posts(models.Model):
    title=models.CharField(max_length=2000)
    image=models.ImageField(upload_to="postimages",null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userposts")
    created_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name="post_like")

    def __str__(self):
        return self.title
    


class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment") 
    comment_text=models.CharField(max_length=200)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="post_comment") #a single post can have many comments
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text
###################################################################################################
###################################################################################################
 

# django signals:   post_save,  pre_save,  post_delete,  pre_delete

# this is done whenever a user is created, its profile object needs tobe created
def create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)
# post.save: used bcoz, after creating/saving a user in User model then needs to create the profile object