# Generated by Django 5.1 on 2024-08-20 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_project_shot_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='consent_form',
        ),
        migrations.AlterField(
            model_name='project',
            name='shot_list',
            field=models.ManyToManyField(blank=True, related_name='projects', to='api.shotlist'),
        ),
        migrations.AddField(
            model_name='project',
            name='consent_form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='api.consentform'),
        ),
    ]
