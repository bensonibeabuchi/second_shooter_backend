# Generated by Django 5.1 on 2024-08-28 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_project_slug_alter_shotlist_shot_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shotlist',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AlterField(
            model_name='shotlist',
            name='shot_type',
            field=models.CharField(blank=True, choices=[('extreme-close-up', 'Extreme Close up'), ('close-up', 'Close Up'), ('medium-shot', 'Medium Shot'), ('wide-shot', 'Wide Shot'), ('extreme-wide-shot', 'Extreme Wide Shot')], max_length=512, null=True),
        ),
    ]
