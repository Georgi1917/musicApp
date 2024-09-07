from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FriendList(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="sent_friend_request")
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="received_friend_request")
    status = models.CharField(max_length=30)