from django.urls import path, include
from friends_list import views

urlpatterns = [
    path('friend-list', views.show_friends_list, name="friends-list"),
    path('friends-list/<int:receiver_id>', views.send_friend_request, name="send-request"),
    path('accept-request/<int:sender_id>', views.accept_friend_request, name="accept-request")
]