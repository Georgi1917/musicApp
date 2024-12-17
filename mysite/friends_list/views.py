from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from friends_list.models import FriendRequestList
from album_creation.models import Playlist, FollowedPlaylist
from song_creation.models import Song
from django.db.models import Q
from django.http import Http404
from friends_list.forms import SearchForm
from accounts.models import Profile

UserModel = get_user_model()


@login_required(login_url=settings.LOGIN_URL)
def search_friends(request):
    form = SearchForm()

    search_query = request.GET.get('searched_user', '')

    form.initial["searched_user"] = search_query

    searched_users = UserModel.objects.filter(username__icontains=search_query).exclude(id=request.user.id) if search_query else []

    needed_users = [
        user for user in searched_users
        if (
            (user.id not in list(map(lambda x: x.receiver_id, request.user.sent_friend_request.all()))) and
            (user.id not in list(map(lambda x: x.sender_id, request.user.received_friend_request.all()))) and
            (user.id not in list(map(lambda x: x.user.id, request.user.all_friends.all())))
        )
    ]

    paginator = Paginator(needed_users, 20)

    page_number = request.GET.get("page", 1)

    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "searched_users": page_obj,
        "paginator": paginator,
        "search_query": search_query,
        "page": page_number
    }
    
    return render(request, "friends_list/search_friends.html", context)


@login_required(login_url=settings.LOGIN_URL)
def show_friends_list(request):

    context = {
        "sent_friend_requests": request.user.sent_friend_request.filter(status="Pending").all(),
        "received_friend_requests": request.user.received_friend_request.filter(status="Pending").all(),
        "friends_list": request.user.all_friends.all()
    }

    return render(request, 'friends_list/friends_list.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
def send_friend_request(request, receiver_id):

    receiver = get_object_or_404(UserModel, id=receiver_id)

    if receiver == request.user:

        raise Http404

    if receiver in list(map(lambda x: x.user, request.user.all_friends.all())):

        raise Http404

    if not (receiver.received_friend_request.filter(status="Pending", sender=request.user)) and not (request.user.received_friend_request.filter(status="Pending", sender=receiver)):

        FriendRequestList.objects.create(sender=request.user, receiver=receiver, status="Pending")
    
    else:

        raise Http404

    if request.GET.get("ref") == "friends_profile":

        return redirect('see-friends', friend_slug=request.GET.get("friend_slug"))

    else:

        return redirect(f"{reverse_lazy('find-friends')}?searched_user={request.GET.get("searched_user", "")}&page={request.GET.get("page", 1)}")


@login_required(login_url=settings.LOGIN_URL)
def accept_friend_request(request, sender_id):

    sender_user = get_object_or_404(UserModel, id=sender_id)
    friend_request = get_object_or_404(FriendRequestList, sender=sender_user, receiver=request.user)
        
    if sender_user not in request.user.all_friends.all():
        request.user.main_friend.friends.add(sender_user)

    if request.user not in sender_user.all_friends.all():
        sender_user.main_friend.friends.add(request.user)

    friend_request.delete()

    return redirect("friends-list")


@login_required(login_url=settings.LOGIN_URL)
def see_friends_profile(request, friend_slug):

    friend = get_object_or_404(Profile, slug=friend_slug)

    if friend.user not in [x.user for x in request.user.all_friends.all()]:

        raise Http404

    context = {
        "friend": friend,
    }
    
    return render(request, 'friends_list/friend_profile.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
def see_friends_playlists(request, friend_slug):

    friend = get_object_or_404(Profile, slug=friend_slug)

    if friend.user not in [x.user for x in request.user.all_friends.all()]:

        raise Http404

    context = {
        "friend_playlists": Playlist.objects.filter(user_id=friend.id),
        "friend": friend,
        "followed_playlists": list(map(lambda x: x.playlist, request.user.followed_playlists.all()))
    }

    return render(request, "friends_list/friend-playlists.html", context)


@login_required(login_url=settings.LOGIN_URL)
def see_friends_songs(request, friend_slug, friend_album_id):

    songs = Song.objects.filter(album_id=friend_album_id)

    friend = get_object_or_404(Profile, slug=friend_slug)

    if friend.user not in [x.user for x in request.user.all_friends.all()]:

        raise Http404

    context = {
        "songs": songs,
        "friend_slug": friend_slug,
    }
    
    return render(request, 'friends_list/friend_songs.html', context=context)


@login_required(login_url=settings.LOGIN_URL)
def see_friends_friendlist(request, friend_slug):

    friend_user = get_object_or_404(Profile, slug=friend_slug)

    if friend_user.user not in [x.user for x in request.user.all_friends.all()]:

        raise Http404

    pending_request_in_list = FriendRequestList.objects.filter(
        (Q(sender_id=request.user.id) | Q(receiver_id=request.user.id)) & Q(status="Pending")
    )

    context = {
        "friend_user": friend_user,
        "friends_list": friend_user.user.all_friends.all(),
        "logged_in_list": request.user.all_friends.all(),
        "pending_requests_senders_ids": list(map(lambda x: x.sender_id, pending_request_in_list)),
        "pending_requests_receivers_ids": list(map(lambda x: x.receiver_id, pending_request_in_list))
    }

    return render(request, "friends_list/friends_friend_list.html", context=context)


@login_required(login_url=settings.LOGIN_URL)
def see_friends_posts(request, friend_slug):

    friend_user = get_object_or_404(Profile, slug=friend_slug)

    if friend_user.user not in [x.user for x in request.user.all_friends.all()]:

        raise Http404

    context = {
        "friend_user": friend_user,
        "posts": friend_user.user.forums.all(),
        "likes": list(map(lambda x: x.post, request.user.likes.all())),
    }

    return render(request, "friends_list/friend-posts.html", context)


@login_required(login_url=settings.LOGIN_URL)
def remove_friend_request(request, friend_request_id):

    needed_obj = FriendRequestList.objects.filter(pk=friend_request_id).first()

    if needed_obj:

        needed_obj.delete()

    return redirect('friends-list')


@login_required(login_url=settings.LOGIN_URL)
def remove_friend(request, friend_id):
    
    friend_user = get_object_or_404(UserModel, pk=friend_id)

    if friend_user not in [x.user for x in request.user.all_friends.all()]:

        raise Http404

    if friend_user in list(map(lambda x: x.user, request.user.all_friends.all())):
        request.user.main_friend.friends.remove(friend_user)
        friend_user.main_friend.friends.remove(request.user)

    return redirect('friends-list')


@login_required(login_url=settings.LOGIN_URL)
def follow_playlist(request, friend_slug, playlist_id):

    friend_user = get_object_or_404(Profile, slug=friend_slug)

    if friend_user.user not in [x.user for x in request.user.all_friends.all()]:

        raise Http404

    playlist = get_object_or_404(Playlist, id=playlist_id)
    
    followed_playlist = FollowedPlaylist.objects.filter(user=request.user, playlist=playlist).first()

    if followed_playlist:

        followed_playlist.delete()

    else:

        FollowedPlaylist.objects.create(user=request.user, playlist=playlist)

    return redirect("see-playlists", friend_slug=friend_slug)