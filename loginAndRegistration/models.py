from datetime import time
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.http import request
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.urls import reverse


class Profile(models.Model):
    GENDER_CHOICE = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICE, default="M", max_length=1)
    email = models.EmailField(max_length=200, blank=True)
    bio = models.TextField(default="no bio...", max_length=300)
    private = models.BooleanField(default=False)
    country = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(default=timezone.now)
    avatar = models.ImageField(default="avatar.png", upload_to="avatars/")
    friends = models.ManyToManyField(
        User, blank=True, related_name="friends", through="relation"
    )
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def accepted(self):
        return self.friends.all().filter(request_status="A")


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(
        upload_to="posts",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
        blank=True,
    )
    liked = models.ManyToManyField(Profile, blank=True, related_name="likes")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.liked.all().count()

    class Meta:
        ordering = ("-created",)


class relation(models.Model):
    f_request = (("A", "Accepted"), ("P", "Pending"))
    sr = (("S", "Sender"), ("R", "Receiver"))
    friend1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend1")
    friend2 = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="friend2",
        verbose_name="Friend Request accepted or pending",
    )
    sender_or_receiver = models.CharField(max_length=12, choices=sr)
    request_status = models.CharField(max_length=10, choices=f_request)

    def __str__(self):
        return f"{self.friend1} send friend request to {self.friend2.user} and the status is {self.request_status}"
