# Generated by Django 5.0.6 on 2024-11-27 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_likecomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentpost',
            name='upvotes',
        ),
        migrations.RemoveField(
            model_name='forumpost',
            name='number_of_comments',
        ),
        migrations.RemoveField(
            model_name='forumpost',
            name='upvotes',
        ),
    ]