# Generated by Django 5.1 on 2024-08-20 16:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_project_consent_form_project_consent_form'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='collaborators',
            field=models.ManyToManyField(blank=True, related_name='collaborated_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='consent_form',
            field=models.ManyToManyField(blank=True, related_name='projects', to='api.consentform'),
        ),
    ]
