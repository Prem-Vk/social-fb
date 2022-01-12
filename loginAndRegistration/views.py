from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserProfileForm,
    UserEditForm,
    UserProfileEditForm,
    PostForm,
)
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Comment, Profile, Post, relation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def UserLogin(request):
    form = LoginForm()
    if request.user.is_superuser:
        logout(request)
        return render(request, "loginAndRegistration/logout.html")
    elif request.method == "POST":
        form = LoginForm(request.POST)
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
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.slug = new_user.username.replace(" ", "-")
            new_profile.save()
            return redirect(reverse("login:login"))
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
    return redirect(reverse("login:login"))


@login_required
def home_page(request, username):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES, prefix="post")
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = profile
            post.save()
    post_form = PostForm(prefix="post")
    all_friends = relation.objects.filter(friend1=request.user, request_status="A")
    user_post = Post.objects.filter(author=request.user.profile)
    all_posts = Post.objects.filter(
        author__in=[people.friend2 for people in all_friends]
    ).union(user_post)
    if len(all_posts) == 0:
        all_posts = None
    elif len(all_friends) == 0:
        pass
    else:
        all_posts = (
            Post.objects.filter(author__in=[people.friend2 for people in all_friends])
            .union(user_post)
            .order_by("-updated")
        )
    return render(
        request,
        "home/home.html",
        {
            "user": request.user,
            "profile": profile,
            "post_form": post_form,
            "all_posts": all_posts,
            "all_friends": all_friends,
        },
    )


@login_required
def profile_detail(request, user):
    profile = Profile.objects.get(user=request.user)
    all_post = Post.objects.filter(author=profile)
    all_friends = relation.objects.filter(friend1=request.user, request_status="A")
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = UserProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            profile = Profile.objects.get(user=request.user)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "profile/profile.html",
        {
            "profile": profile,
            "user_form": user_form,
            "profile_form": profile_form,
            "all_post": all_post,
            "all_friends": all_friends,
        },
    )


@login_required
@transaction.atomic
def SearchFriend(request):
    pending = []
    accepted = []
    if request.method == "POST":
        search = request.POST.get("search")
        status_pending = request.POST.get("pending")
        status_accepted = request.POST.get("accepted")
        status_new = request.POST.get("new")
        cancel = request.POST.get("cancel")
        find = search.split(" ")
        if status_pending is not None:
            pend_user = User.objects.get(username=status_pending)
            accept1 = relation.objects.get(
                friend1=request.user, friend2=pend_user.profile
            )
            accept2 = relation.objects.get(
                friend1=pend_user,
                friend2=request.user.profile,
            )
            accept1.request_status = "A"
            accept2.request_status = "A"
            accept1.save()
            accept2.save()
        if status_accepted is not None:
            pass
        if status_new is not None:
            pend_new = User.objects.get(username=status_new)
            relation.objects.create(
                friend1=request.user,
                friend2=pend_new.profile,
                sender_or_receiver="S",
                request_status="P",
            )
            relation.objects.create(
                friend1=pend_new,
                friend2=request.user.profile,
                sender_or_receiver="R",
                request_status="P",
            )
        if cancel is not None:
            cancel_request = User.objects.get(username=cancel)
            sender = relation.objects.get(
                friend1=cancel_request, friend2=request.user.profile, request_status="P"
            )
            receiver = relation.objects.get(
                friend1=request.user, friend2=cancel_request.profile, request_status="P"
            )
            sender.delete()
            receiver.delete()
        if len(find) == 1:
            friends = Profile.objects.filter(
                Q(first_name__icontains=find[0]) | Q(last_name__icontains=find[0])
            ).filter(~Q(user=request.user))
        else:
            friends = Profile.objects.filter(
                Q(first_name__icontains=find[0]) & Q(last_name__icontains=find[1])
            ).filter(~Q(user=request.user))
        relations = relation.objects.filter(friend1=request.user)
        previous_relations = [req.friend2.user for req in relations]
        for friend in friends:
            for rel in relations:
                if friend.user == rel.friend2.user:
                    if rel.request_status == "P":
                        pending.append(rel)
                    else:
                        accepted.append(friend.user)
        return render(
            request,
            "search/search.html",
            {
                "user": request.user,
                "search": search,
                "friends": friends,
                "relations": relations,
                "previous_relation": previous_relations,
                "pending": pending,
                "accepted": accepted,
                "search": search,
            },
        )
    else:
        return redirect(
            reverse("login:home", kwargs={"username": request.user.username})
        )


def login_redirect(request):
    return redirect(reverse("login:login"))


@login_required
@transaction.atomic
def friends_page(request):
    if request.method == "POST":
        status_pending = request.POST.get("accept")
        reject = request.POST.get("reject")
        unfriend = request.POST.get("unfriend")
        if status_pending is not None:
            pend_user = User.objects.get(username=status_pending)
            accept1 = relation.objects.get(
                friend1=request.user, friend2=pend_user.profile
            )
            accept2 = relation.objects.get(
                friend1=pend_user,
                friend2=request.user.profile,
            )
            accept1.request_status = "A"
            accept2.request_status = "A"
            accept1.save()
            accept2.save()
        if reject is not None:
            pend_user = User.objects.get(username=reject)
            reject1 = relation.objects.get(
                friend1=request.user, friend2=pend_user.profile, request_status="P"
            )
            reject2 = relation.objects.get(
                friend1=pend_user, friend2=request.user.profile, request_status="P"
            )
            reject1.delete()
            reject2.delete()
        if unfriend is not None:
            pend_user = User.objects.get(username=unfriend)
            friend1 = relation.objects.get(
                friend1=request.user, friend2=pend_user.profile, request_status="A"
            )
            friend2 = relation.objects.get(
                friend1=pend_user, friend2=request.user.profile, request_status="A"
            )
            friend1.delete()
            friend2.delete()
        friends = relation.objects.filter(friend1=request.user, request_status="A")
        new_friends = relation.objects.filter(friend1=request.user, request_status="P")
    else:
        friends = relation.objects.filter(friend1=request.user, request_status="A")
        new_friends = relation.objects.filter(friend1=request.user, request_status="P")
    return render(
        request,
        "friends/friends.html",
        {"friends": friends, "new_friends": new_friends},
    )


@login_required
def post_comment(request, pk):
    relations = []
    author = Post.objects.get(id=pk)
    try:
        if request.user == author.author.user:
            if request.method == "POST":
                body = request.POST.get("comment-body")
                post_id = request.POST.get("post-id")
                post = Post.objects.get(id=post_id)
                Comment.objects.create(user=request.user.profile, post=post, body=body)
            posts = Post.objects.get(id=pk)
            comments = Comment.objects.filter(post=posts)
            return render(
                request,
                "posts/post.html",
                {"posts": posts, "comments": comments, "pk": pk},
            )
        elif relation.objects.get(
            friend1=request.user, friend2=author.author, request_status="A"
        ):
            if request.method == "POST":
                body = request.POST.get("comment-body")
                post_id = request.POST.get("post-id")
                post = Post.objects.get(id=post_id)
                Comment.objects.create(user=request.user.profile, post=post, body=body)
            posts = Post.objects.get(id=pk)
            comments = Comment.objects.filter(post=posts)
            return render(
                request,
                "posts/post.html",
                {"posts": posts, "comments": comments, "pk": pk},
            )
        else:
            return HttpResponse("Invalid Id")
    except ObjectDoesNotExist:
        return HttpResponse("Invalid ID")


@login_required
def like_counter(request):
    if request.method == "POST":
        unlike = request.POST.get("unlike")
        like = request.POST.get("like")
        page = request.POST.get("page")
        if like is not None:
            post = get_object_or_404(Post, id=like)
            post.liked.add(request.user.profile)
        else:
            post = get_object_or_404(Post, id=unlike)
            post.liked.remove(request.user.profile)
        if page == "profile":
            return redirect(
                reverse("login:profile", kwargs={"user": request.user.username})
            )
    return redirect(reverse("login:home", kwargs={"username": request.user.username}))
