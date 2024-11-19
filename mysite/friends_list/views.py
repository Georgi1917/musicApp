from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from friends_list.models import FriendRequestList, FriendList
from album_song_creation.models import Playlist
from song_creation.models import Song
from django.db.models import Q
from friends_list.forms import SearchForm

# Create your views here.


def search_friends(request):
    form = SearchForm()

    search_query = request.GET.get('searched_user', '')

    form.initial["searched_user"] = search_query

    searched_users = User.objects.filter(username__icontains=search_query).exclude(id=request.user.id) if search_query else []

    needed_users = [
        user for user in searched_users
        if (
            (user.id not in list(map(lambda x: x.receiver_id, request.user.sent_friend_request.all()))) and
            (user.id not in list(map(lambda x: x.sender_id, request.user.received_friend_request.all()))) and
            (user.id not in list(map(lambda x: x.user.id, request.user.all_friends.all())))
        )
    ]


    context = {
        "form": form,
        "searched_users": needed_users
    }
    
    return render(request, "friends_list/search_friends.html", context)


def show_friends_list(request):

    context = {
        "sent_friend_requests": request.user.sent_friend_request.filter(status="Pending").all(),
        "received_friend_requests": request.user.received_friend_request.filter(status="Pending").all(),
        "friends_list": request.user.all_friends.all()
    }

    return render(request, 'friends_list/friends_list.html', context=context)


def send_friend_request(request, receiver_id):

    receiver = get_object_or_404(User, id=receiver_id)

    FriendRequestList.objects.create(sender=request.user, receiver=receiver, status="Pending")

    return redirect("friends-list")


def accept_friend_request(request, sender_id):
    sender_user = User.objects.get(pk=sender_id)

    friend_list_receiver = FriendList.objects.filter(user=request.user).first()

    print(request.user.main_friend.first())

    if not friend_list_receiver:
        friend_list_receiver = FriendList.objects.create(user=request.user)
        
    if sender_user not in friend_list_receiver.friends.all():
        friend_list_receiver.friends.add(sender_user)


    friend_list_sender = FriendList.objects.filter(user=sender_user).first()

    print(sender_user.main_friend.first())

    if not friend_list_sender:
        friend_list_sender = FriendList.objects.create(user=sender_user)

    if request.user not in friend_list_sender.friends.all():
        friend_list_sender.friends.add(request.user)

    print(sender_user.main_friend.first())

    friend_request = FriendRequestList.objects.get(
        Q(receiver_id=request.user.id) & Q(sender_id=sender_id)
    )

    friend_request.status = "Accepted"
    friend_request.save()

    return redirect("friends-list")


def see_friends_profile(request, friend_id):

    friend_playlists = Playlist.objects.filter(user_id=friend_id)

    context = {
        "friend_playlists": friend_playlists,
        "friend_id": friend_id,
    }
    
    return render(request, 'friends_list/friend_profile.html', context=context)


def see_friends_songs(request, friend_id, friend_album_id):
    songs = Song.objects.filter(album_id=friend_album_id)

    context = {
        "songs": songs
    }
    
    return render(request, 'friends_list/friend_songs.html', context=context)


def see_friends_friendlist(request, friend_id):

    friend_user = get_object_or_404(User, pk=friend_id)

    pending_request_in_list = FriendRequestList.objects.filter(
        (Q(sender_id=request.user.id) | Q(receiver_id=request.user.id)) & Q(status="Pending")
    )

    context = {
        "friends_list": friend_user.all_friends.all(),
        "logged_in_list": request.user.all_friends.all(),
        "pending_requests_senders_ids": list(map(lambda x: x.sender_id, pending_request_in_list)),
        "pending_requests_receivers_ids": list(map(lambda x: x.receiver_id, pending_request_in_list))
    }

    return render(request, "friends_list/friends_friend_list.html", context=context)