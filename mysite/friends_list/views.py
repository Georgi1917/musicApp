from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from friends_list.models import FriendRequestList
from album_creation.models import Playlist, FollowedPlaylist
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

    paginator = Paginator(needed_users, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "searched_users": page_obj,
        "paginator": paginator,
        "search_query": search_query
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

    if not (receiver.received_friend_request.all().filter(Q(status="Pending") & Q(sender=request.user))):
        FriendRequestList.objects.create(sender=request.user, receiver=receiver, status="Pending")

    return redirect("friends-list")


def accept_friend_request(request, sender_id):
    sender_user = User.objects.get(pk=sender_id)
        
    if sender_user not in request.user.all_friends.all():
        request.user.main_friend.friends.add(sender_user)

    if request.user not in sender_user.all_friends.all():
        sender_user.main_friend.friends.add(request.user)

    friend_request = FriendRequestList.objects.get(
        Q(receiver_id=request.user.id) & Q(sender_id=sender_id)
    )

    friend_request.delete()

    return redirect("friends-list")


def see_friends_profile(request, friend_id):

    context = {
        "friend_playlists": Playlist.objects.filter(user_id=friend_id),
        "friend_id": friend_id,
        "followed_playlists": list(map(lambda x: x.playlist , request.user.followed_playlists.all()))
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


def remove_friend_request(request, friend_request_id):

    needed_obj = FriendRequestList.objects.get(pk=friend_request_id)
    needed_obj.delete()

    return redirect('friends-list')


def remove_friend(request, friend_id):
    
    friend_user = get_object_or_404(User, pk=friend_id)

    if friend_user in list(map(lambda x: x.user, request.user.all_friends.all())):
        request.user.main_friend.friends.remove(friend_user)
        friend_user.main_friend.friends.remove(request.user)

    return redirect('friends-list')


def follow_playlist(request, friend_id, playlist_id):

    playlist = Playlist.objects.get(id=playlist_id)
    
    followed_playlist = FollowedPlaylist.objects.filter(user=request.user, playlist=playlist).first()

    if followed_playlist:

        followed_playlist.delete()

    else:

        FollowedPlaylist.objects.create(user=request.user, playlist=playlist)

    return redirect("see-profile", friend_id=friend_id)