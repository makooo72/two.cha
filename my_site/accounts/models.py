from django.db import models
from django.contrib.auth.models import User

class ForumUser(models.Model):
    description = models.TextField(blank=True, null=True)
    photo_path = models.ImageField(upload_to='images/%Y/%m/%d/%H/', blank=True)
    user = models.OneToOneField(User, related_name="forum_user", on_delete=models.CASCADE)
    subscubes = models.ManyToManyField("self", through="Subscription")

    def save(self, *args, **kwargs):
        if self.photo_path == "" or self.photo_path is None:
            self.photo_path = "images/based/1.png"
        super().save(*args, **kwargs)

class Subscription(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} → {self.following}"
