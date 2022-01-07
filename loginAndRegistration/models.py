from datetime import time
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse


class Profile(models.Model):
    GENDER_CHOICE = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICE, default="M", max_length=1)
    email = models.EmailField(max_length=200, blank=True)
    bio = models.TextField(default="no bio...", max_length=300)
    country = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(default=timezone.now)
    avatar = models.ImageField(default="avatar.png", upload_to="avatars/")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
