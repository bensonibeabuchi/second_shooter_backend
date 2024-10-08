# Generated by Django 5.1 on 2024-08-20 11:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_consentform_agency_logo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='consentform',
            name='agency_logo',
            field=models.ImageField(blank=True, null=True, upload_to='images/agency_logo'),
        ),
        migrations.AddField(
            model_name='project',
            name='consent_form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='api.consentform'),
        ),
    ]
