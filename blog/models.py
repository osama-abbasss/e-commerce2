from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.shortcuts import reverse
from django.conf import settings



class Post(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length= 35)
    content = RichTextField()
    description= models.CharField(max_length= 170)
    img = models.ImageField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse ('blog:single_post', kwargs={'slug': self.slug})



class Comment(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length= 350)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
