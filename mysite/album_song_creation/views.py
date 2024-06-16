from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def show_album_creation_page(request, user_id):
    return render(request, 'create-album.html')