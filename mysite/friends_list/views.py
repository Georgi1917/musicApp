from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from friends_list.models import FriendRequestList, FriendList
from django.db.models import Q

# Create your views here.

def show_friends_list(request, user_id):
    searched_user = request.GET.get('searched_names', '')

    users = User.objects.filter(username__icontains=searched_user) if searched_user else []

    sent_friend_requests = FriendRequestList.objects.filter(
        Q(sender_id=request.user.id) & Q(status="Pending")
    )

    received_friend_requests = FriendRequestList.objects.filter(
        Q(receiver_id=request.user.id) & Q(status="Pending")
    )

    friends_list = FriendList.objects.get(user_id=user_id).friends.all()

    needed_users = [
        x for x in users
        if (
        (x.pk not in list(map(lambda x: x.receiver_id, sent_friend_requests))) and
        (x.pk not in list(map(lambda x: x.sender_id,received_friend_requests))) and
        (x not in friends_list) and
        (x.pk != request.user.id))
    ]

    context = {
        "users": needed_users,
        "searched_user": searched_user,
        "sent_friend_requests": sent_friend_requests,
        "received_friend_requests": received_friend_requests,
        "friends_list": friends_list
    }

    return render(request, 'friends_list.html', context=context)

def send_friend_request(request, user_id, receiver_id):
    sender = get_object_or_404(User, id=user_id)
    receiver = get_object_or_404(User, id=receiver_id)

    friend_request = FriendRequestList.objects.create(sender=sender, receiver=receiver, status="Pending")

    return redirect("friends-list", user_id=user_id)

def accept_friend_request(request, user_id, sender_id):
    sender_user = User.objects.get(pk=sender_id)
    receiver_user = User.objects.get(pk=user_id)

    friend_list_receiver = FriendList.objects.filter(user=receiver_user).first()

    if not friend_list_receiver:
        friend_list_receiver = FriendList.objects.create(user=receiver_user)
        
        if sender_user not in friend_list_receiver.friends.all():
            friend_list_receiver.friends.add(sender_user)

    else:

        if sender_user not in friend_list_receiver.friends.all():
            friend_list_receiver.friends.add(sender_user)

    friend_list_sender = FriendList.objects.filter(user=sender_user).first()

    if not friend_list_sender:
        friend_list_sender = FriendList.objects.create(user=sender_user)

        if receiver_user not in friend_list_sender.friends.all():
            friend_list_sender.friends.add(receiver_user)

    else:

        if receiver_user not in friend_list_sender.friends.all():
            friend_list_sender.friends.add(receiver_user)

    friend_request = FriendRequestList.objects.get(
        Q(receiver_id=user_id) & Q(sender_id=sender_id)
    )
    friend_request.status = "Accepted"
    friend_request.save()

    print(friend_list_receiver.friends.all())
    print(friend_list_sender.friends.all())

    return redirect("friends-list", user_id=user_id)

    