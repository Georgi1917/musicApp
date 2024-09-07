from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from friends_list.models import FriendList

# Create your views here.

def show_friends_list(request, user_id):
    searched_user = request.GET.get('searched_names', '')
    users = User.objects.filter(username__icontains=searched_user) if searched_user else []
    sent_friend_requests = FriendList.objects.filter(sender_id=request.user.id)
    received_friend_requests = FriendList.objects.filter(receiver_id=request.user.id)

    context = {
        "users": users,
        "searched_user": searched_user,
        "sent_friend_requests": sent_friend_requests,
        "received_friend_requests": received_friend_requests
    }

    return render(request, 'friends_list.html', context=context)

def send_friend_request(request, user_id, receiver_id):
    sender = get_object_or_404(User, id=user_id)
    receiver = get_object_or_404(User, id=receiver_id)

    friend_request = FriendList.objects.create(sender=sender, receiver=receiver, status="Pending")

    return redirect("friends-list", user_id=user_id)