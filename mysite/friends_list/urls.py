from django.urls import path, include
from friends_list import views

urlpatterns = [
    path('friend-list/', views.show_friends_list, name="friends-list"),
    path('friend-list/remove/<int:friend_id>/', views.remove_friend, name="remove-friend"),
    path('friend-list/remove-request/<int:friend_request_id>/', views.remove_friend_request, name="remove-request"),
    path('find-friends/', views.search_friends, name="find-friends"),
    path('friends-list/<int:receiver_id>/', views.send_friend_request, name="send-request"),
    path('accept-request/<int:sender_id>/', views.accept_friend_request, name="accept-request"),
    path('friend/<int:friend_id>/', views.see_friends_profile, name="see-profile"),
    path('friend/<int:friend_id>/songs/<int:friend_album_id>/', views.see_friends_songs, name="see-songs"),
    path('friend/<int:friend_id>/friends/', views.see_friends_friendlist, name="see-friends")
]