from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.views.generic import CreateView,FormView,TemplateView,UpdateView,ListView,DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout

from myapp.forms import SignUpForm,LogInForm,ProfileEditForm,PostForm,CoverPicForm
from myapp.models import UserProfile,Posts,Comments

# Registeration
class SignUpView(CreateView):
    model=User
    form_class=SignUpForm
    template_name="register.html"
    success_url=reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request,"account has been created")
        return super().form_valid(form)
    

    def form_invalid(self, form) :
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)
    
# Login
class SignInView(FormView):
    form_class=LogInForm
    template_name="login.html"
  
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login successull")
                return redirect("index")
            messages.error(request,"invalid credentials")
        return render(request,self.template_name,{"form":form})
    
# index : now to add posts
class IndexView(CreateView,ListView):
    model=Posts
    form_class=PostForm
    template_name="index.html"
    context_object_name="posts"
    success_url=reverse_lazy("index")

# need to pass value to 'user' field in the form (ie, the loggined user)
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


#userprofile update
class ProfileEditView(UpdateView):
    model=UserProfile
    form_class=ProfileEditForm
    template_name="profile_edit.html"
    success_url=reverse_lazy("index")



# localhost:8000/posts/1/like/ 
#  to like the post's by a loggined user
def add_like_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    post_obj=Posts.objects.get(id=id)  #taken the post objct
    post_obj.liked_by.add(request.user) # and used add() method to get liked and passed the loggined user
    return redirect("index")


# localhost:8000/posts/{id}/comments/add/
# to add comments to a post
def add_comment_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    post_obj=Posts.objects.get(id=id)  #taken the post objct
    comment=request.POST.get("comment") #taken the comment from the name attribute
    user=request.user #taken the user
    Comments.objects.create(user=user,comment_text=comment,post=post_obj) #create a comment by looking to Comments Model
    return redirect("index")


# localhost:8000/comments/{id}/remove
# to remove a comment
def remove_comment_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    comment_obj=Comments.objects.get(id=id)
    if request.user==comment_obj.user:  #loggined user & commented user must be same then only allows to delete the comment
        comment_obj.delete()
        return redirect("index")
    else:
        messages.error(request,"please contact admin")
        return redirect("login")



# profile detail view
# localhost:8000/profiles/{id}/

class ProfileDetailView(DetailView):
    model=UserProfile
    template_name="profile.html"
    context_object_name="profile"


# cover pic change view
# localhost:8000/profile/{id}/coverpic/change

def change_cover_pic_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    prof_obj=UserProfile.objects.get(id=id)
    form=CoverPicForm(instance=prof_obj,data=request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("profiledetail",pk=id) #pk=id, need to pass for all redirect with id's(kwargs)
    return redirect("profiledetail",pk=id)
  


# profile list
# localhost:8000/profiles/all/

class ProfileListView(ListView):
    model=UserProfile
    template_name="profile-list.html"
    context_object_name="profiles"

# to change the orm query: here no need to list the loggined user
    def get_queryset(self):
        return UserProfile.objects.exclude(user=self.request.user)



# to follow functionality
# localhost:8000/profile/{id}/follow/

def follow_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    profile_obj=UserProfile.objects.get(id=id) 
    user_prof=request.user.profile #loggined users profile
    user_prof.following.add(profile_obj) #here, profile_obj is added to loggined users 'following' attribute
    user_prof.save()
    return redirect("index")


# unfollow view
# localhost:8000/profile/{id}/unfollow/

def unfollow_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    profile_obj=UserProfile.objects.get(id=id) 
    user_prof=request.user.profile #loggined users profile
    user_prof.following.remove(profile_obj) #here, profile_obj is removed from loggined users 'following' attribute
    user_prof.save()
    return redirect("index")



# post delete view
# localhost:8000/posts/{id}/remove/
def post_delete_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    Posts.objects.get(id=id).delete()
    return redirect("index")




# signout view
def sign_out_view(request,*args,**kwargs):
    logout(request)
    messages.success(request,"succesfully loggedout")
    return redirect("login")

