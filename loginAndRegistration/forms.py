from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import widgets
from .models import Profile, Post


class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        max_length=30,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    password = forms.CharField(
        min_length=8,
        max_length=63,
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        min_length=8,
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    password2 = forms.CharField(
        min_length=8,
        label="",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Username"})
    )

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]


class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    first_name = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "first name"})
    )
    last_name = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "last name"})
    )
    email = forms.EmailField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Email"})
    )

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "gender", "birth_date")


class UserProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        label="First Name", widget=forms.TextInput(attrs={"placeholder": "first name"})
    )
    last_name = forms.CharField(
        label="Last Name", widget=forms.TextInput(attrs={"placeholder": "last name"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.TextInput(attrs={"placeholder": "first name"})
    )
    birth_date = forms.DateField(
        label="Birth Date", widget=forms.DateInput(attrs={"type": "date"})
    )
    private = forms.BooleanField(label="Private Profile", required=False)
    bio = forms.CharField(
        label="Bio",
        widget=forms.Textarea(attrs={"rows": 3, "cols": 35, "placeholder": "Your Bio"}),
    )

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "email",
            "gender",
            "birth_date",
            "private",
            "bio",
            "country",
            "avatar",
        )


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        label="Username ", widget=forms.TextInput(attrs={"placeholder": "Username"})
    )

    class Meta:
        model = User
        fields = ("username",)


class PostForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "What's on your mind today?"}),
    )
    image = forms.ImageField(label="")

    class Meta:
        model = Post
        fields = ["content", "image"]
