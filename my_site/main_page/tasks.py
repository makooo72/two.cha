from .models import Post
from PIL import Image
from io import BytesIO
import os
#from django.dispatch import receiver
#from django.db.models.signals import post_save
from django.core.files.base import ContentFile
from celery import shared_task

@shared_task
def image_processing(id):
    instance = Post.objects.get(id=id)

    original_path = instance.photo_path.path

    with Image.open(instance.photo_path) as photo:
        webp_io = BytesIO()
        photo.save(webp_io, "WEBP", quality=50,
                method=6,
                optimize=True)

        instance.photo_path.save(
            f'{os.path.splitext(os.path.basename(instance.photo_path.name))[0]}.webp',
            ContentFile(webp_io.getvalue())
        )

    if os.path.exists(original_path):
        os.remove(original_path)
    