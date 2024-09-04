# Generated by Django 5.1 on 2024-08-28 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_shotlist_shot_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='shotlist',
            name='shot_type',
            field=models.CharField(blank=True, choices=[('extreme-close-up', 'extreme-close-up'), ('close-up', 'close-up'), ('medium-shot', 'medium-shot'), ('wide-shot', 'wide-shot'), ('extreme-wide-shot', 'extreme-wide-shot')], max_length=512, null=True),
        ),
    ]
