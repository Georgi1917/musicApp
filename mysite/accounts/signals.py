import os
import time
from friends_list.models import FriendList
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from accounts.async_operations import send_mail_async


UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_friend_list(sender, instance, created, **kwargs):
    
    if created:
        FriendList.objects.create(user=instance)
        Profile.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
async def send_welcome_email(sender, instance, created, **kwargs):

    if created:

        await send_mail_async(
            f"Welcome {instance.username}, to The Best Web Music Player",
            "We hope that you enjoy using our application. Remember that your appreciation means a lot to us \n\nBest Wishes, The Loop Play Team!",
            os.getenv("SENDER_EMAIL"),
            [instance.email],
        )
