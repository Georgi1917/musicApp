# Generated by Django 5.0.6 on 2024-07-31 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song_creation', '0004_song_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='duration',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
