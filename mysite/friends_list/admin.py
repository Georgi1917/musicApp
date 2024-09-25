from django.contrib import admin
from friends_list.models import FriendRequestList, FriendList

# Register your models here.

admin.site.register(FriendRequestList)
admin.site.register(FriendList)