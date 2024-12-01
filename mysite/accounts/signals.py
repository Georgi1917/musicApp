from friends_list.models import FriendList
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_friend_list(sender, instance, created, **kwargs):
    
    if created:
        FriendList.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)
