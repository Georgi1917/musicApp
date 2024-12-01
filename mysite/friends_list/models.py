from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class FriendRequestList(models.Model):
    sender = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="sent_friend_request")
    receiver = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="received_friend_request")
    status = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.sender.username}  --  {self.receiver.username} | Status: {self.status}"
    

class FriendList(models.Model):
    user = models.OneToOneField(to=UserModel, on_delete=models.CASCADE, related_name="main_friend")
    friends = models.ManyToManyField(to=UserModel, related_name="all_friends")

    def __str__(self):
        return f"{self.user.username}"