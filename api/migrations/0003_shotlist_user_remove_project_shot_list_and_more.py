# Generated by Django 5.1 on 2024-08-10 22:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shotlist',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='shot_lists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='project',
            name='shot_list',
        ),
        migrations.AddField(
            model_name='project',
            name='shot_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='api.shotlist'),
        ),
    ]
