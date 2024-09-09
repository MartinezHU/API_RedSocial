from django.contrib import admin

from .models import Post, PostImage, Comment, Like, Dislike, Reaction, SharePost

# Register your models here.

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Reaction)
admin.site.register(SharePost)
admin.site.register(Comment)
