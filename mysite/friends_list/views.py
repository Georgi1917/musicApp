from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.

def show_friends_list(request, user_id):
    searched_user = request.GET.get('searched_names', '')
    users = User.objects.filter(username__icontains=searched_user) if searched_user else []

    context = {
        "users": users,
        "searched_user": searched_user
    }

    return render(request, 'friends_list.html', context=context)