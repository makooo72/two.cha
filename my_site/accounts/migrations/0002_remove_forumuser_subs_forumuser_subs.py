# Generated by Django 5.1.6 on 2025-03-15 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumuser',
            name='subs',
        ),
        migrations.AddField(
            model_name='forumuser',
            name='subs',
            field=models.ManyToManyField(related_name='subscubes', to='accounts.forumuser'),
        ),
    ]
