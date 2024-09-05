from django.urls import path, include
from friends_list import views

urlpatterns = [
    path('friend-list', views.show_friends_list, name="friends-list")
]