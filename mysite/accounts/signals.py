from django.contrib.auth.models import User
from friends_list.models import FriendList
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_friend_list(sender, instance, created, **kwargs):
    
    if created:
        FriendList.objects.create(user=instance)
