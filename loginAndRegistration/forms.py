from django import forms
from django.contrib.auth.models import User
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
        min_length=8, label="Password", widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        min_length=8, label="Confirm password", widget=forms.PasswordInput
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

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "gender", "birth_date")


class UserProfileEditForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

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
    class Meta:
        model = User
        fields = ("username",)


class PostForm(forms.ModelForm):
    content = forms.CharField()
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = ["content", "image"]
