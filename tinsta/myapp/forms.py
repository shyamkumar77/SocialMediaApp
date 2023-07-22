from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from myapp.models import UserProfile,Posts


# Registeration form
class SignUpForm(UserCreationForm):

    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]


# Login form
class LogInForm(forms.Form):

    username=forms.CharField()
    password=forms.CharField()


# Userprofile update/edit form
class ProfileEditForm(forms.ModelForm):

    class Meta:
        model=UserProfile
        fields=["profile_pic","bio","address","dob"]
        widgets={
            "profile_pic":forms.FileInput(attrs={"class":"form-control"}),
            "bio":forms.TextInput(attrs={"class":"form-control"}),
            "address":forms.Textarea(attrs={"class":"form-control"}),
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})
            #to get date picker in dob: DateInput and "type":"date"
        }


# PostForm
class PostForm(forms.ModelForm):

    class Meta:
        model=Posts
        fields=["title","image"]


# Coverpic Form
class CoverPicForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["cover_pic"]


    