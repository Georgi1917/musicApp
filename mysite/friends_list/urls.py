from django.urls import path, include
from friends_list import views

urlpatterns = [
    path('friends-list/', views.show_friends_list, name="friends-list"),
    path('friends-list/remove/<int:friend_id>/', views.remove_friend, name="remove-friend"),
    path('friends-list/remove-request/<int:friend_request_id>/', views.remove_friend_request, name="remove-request"),
    path('find-friends/', views.search_friends, name="find-friends"),
    path('friends-list/<int:receiver_id>/', views.send_friend_request, name="send-request"),
    path('accept-request/<int:sender_id>/', views.accept_friend_request, name="accept-request"),
    path('friend/<slug:friend_slug>/', include([
        path('', views.see_friends_profile, name="see-profile"),
        path('playlists/', views.see_friends_playlists, name="see-playlists"),
        path('songs/<int:friend_album_id>/', views.see_friends_songs, name="see-songs"),
        path('follow-playlist/<int:playlist_id>/', views.follow_playlist, name="follow-playlist"),
        path('friends/', views.see_friends_friendlist, name="see-friends"),
        path('posts/', views.see_friends_posts, name="see-posts")
    ])),
]