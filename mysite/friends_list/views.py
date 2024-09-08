from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from friends_list.models import FriendList
from django.db.models import Q

# Create your views here.

def show_friends_list(request, user_id):
    searched_user = request.GET.get('searched_names', '')

    users = User.objects.filter(username__icontains=searched_user) if searched_user else []

    sent_friend_requests = FriendList.objects.filter(
        Q(sender_id=request.user.id) & Q(status="Pending")
    )

    received_friend_requests = FriendList.objects.filter(
        Q(receiver_id=request.user.id) & Q(status="Pending")
    )

    accepted_friends = FriendList.objects.filter(
        Q(sender_id=user_id) | Q(receiver_id=user_id),
        Q(status="Accepted")
    )

    needed_users = [
        x for x in users
        if (
        (x.pk not in list(map(lambda x: x.receiver_id, sent_friend_requests))) and
        (x.pk not in list(map(lambda x: x.sender_id,received_friend_requests))) and
        (x.pk != request.user.id) and
        (x not in accepted_friends))
    ]

    context = {
        "users": needed_users,
        "searched_user": searched_user,
        "sent_friend_requests": sent_friend_requests,
        "received_friend_requests": received_friend_requests,
        "friends": accepted_friends
    }

    return render(request, 'friends_list.html', context=context)

def send_friend_request(request, user_id, receiver_id):
    sender = get_object_or_404(User, id=user_id)
    receiver = get_object_or_404(User, id=receiver_id)

    friend_request = FriendList.objects.create(sender=sender, receiver=receiver, status="Pending")

    return redirect("friends-list", user_id=user_id)