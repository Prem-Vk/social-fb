from django.contrib import admin
from .models import Profile, Post, relation, Comment, Chat

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(relation)
admin.site.register(Comment)
admin.site.register(Chat)
