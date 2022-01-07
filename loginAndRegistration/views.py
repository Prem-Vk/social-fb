from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm, UserProfileForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def UserLogin(request):
    form = LoginForm()
    if request.user.is_superuser:
        logout(request)
        return render(request, "loginAndRegistration/logout.html")
    elif request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        print("suer")
        return render(
            request,
            "home/home.html",
            {"user": request.user, "profile": profile},
        )
    elif request.method == "POST":
        form = LoginForm(request.POST)
        print("suer2")
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    profile = Profile.objects.get(user=user)
                    return redirect(
                        reverse(
                            "login:home", kwargs={"username": request.user.username}
                        )
                    )
                else:
                    return HttpResponse("Disabled User")
            else:
                return HttpResponse("Invalid Login")
    else:
        form = LoginForm()
    return render(request, "loginAndRegistration/login.html", {"form": form})


def UserRegistration(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, prefix="user")
        profile_form = UserProfileForm(request.POST, prefix="profile")
        if user_form.is_valid() and profile_form.is_valid():
            print("done")
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.slug = new_user.username
            new_profile.save()
            return render(
                request,
                "loginAndRegistration/registration_done.html",
                {"new_user": new_user},
            )
    else:
        user_form = UserRegistrationForm(prefix="user")
        profile_form = UserProfileForm(prefix="profile")
    return render(
        request,
        "loginAndRegistration/registration.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def logout_request(request):
    logout(request)
    return render(request, "loginAndRegistration/logout.html")


@login_required
def home_page(request, username):
    profile = Profile.objects.get(user=request.user)
    print("suer3")
    return render(
        request,
        "home/home.html",
        {"user": request.user, "profile": profile},
    )


@login_required
def profile_detail(request, user):
    print("hello")
    profile = Profile.objects.get(user=request.user)
    return render(request, "profile/profile.html", {"profile": profile})
