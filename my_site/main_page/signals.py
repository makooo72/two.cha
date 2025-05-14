from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files.base import ContentFile
from .models import Post
from PIL import Image
from io import BytesIO
import os
from .tasks import image_processing

@receiver(post_save, sender=Post)
def minimalize_size_images(sender, instance, created, **kwargs):
    image_processing.delay(instance.id)