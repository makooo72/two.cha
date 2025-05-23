# Generated by Django 5.1.6 on 2025-03-15 07:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0005_remove_message_message_remove_post_message_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='forum_user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='forum_user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='photo_path',
            field=models.ImageField(upload_to='images/%Y/%m/%d/%H/'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_path', models.ImageField(blank=True, upload_to='images/%Y/%m/%d/%H/')),
                ('likes', models.PositiveSmallIntegerField(default=0)),
                ('description', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main_page.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='tag',
            name='messages',
            field=models.ManyToManyField(related_name='tags', to='main_page.comment'),
        ),
        migrations.DeleteModel(
            name='ForumUser',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
