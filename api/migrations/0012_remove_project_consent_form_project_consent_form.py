# Generated by Django 5.1 on 2024-08-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_project_consent_form_alter_project_shot_list_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='consent_form',
        ),
        migrations.AddField(
            model_name='project',
            name='consent_form',
            field=models.ManyToManyField(blank=True, null=True, related_name='projects', to='api.consentform'),
        ),
    ]
