from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Blog
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "username")


class UpdateUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "username",'gender','country','age','image',"about")


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ["name", "tagline", "description", "blogtype"]
