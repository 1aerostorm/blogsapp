from django.contrib import admin
from .models import Account, Post, Comment

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'content', 'image', 'created_at', 'author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'username', 'content', 'created_at')