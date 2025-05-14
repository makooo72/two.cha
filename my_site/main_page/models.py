from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    photo_path = models.ImageField(upload_to='images/%Y/%m/%d/%H/')
    description = models.TextField()
    likes = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    photo_path = models.ImageField(upload_to='images/%Y/%m/%d/%H/', blank=True)
    likes = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(verbose_name="Прокомментируйте это")
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.description

    
class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    post = models.ManyToManyField(Post, related_name="tags")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.title.startswith("#") is False:
            raise ValidationError("tag not supported")
        super().save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'post'), ('user', 'comment')]