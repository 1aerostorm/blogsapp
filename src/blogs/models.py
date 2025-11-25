from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=320, unique=True)

    def __str__(self):
        return f"{self.username} [{self.email}]"

class Post(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    content = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    username = models.CharField(max_length=16)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return f"{self.id} [{self.username}]"