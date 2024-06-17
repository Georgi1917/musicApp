from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from album_song_creation.models import Playlist

# Create your views here.

def home_page_index(request):
    return render(request, "index.html")

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            curr_user = request.user
            messages.success(request, ("You have been registered succesfully!!"))
            return redirect('main-page', user_id=curr_user.id)
        else:
            messages.success(request, ("There was an error, please try again!"))
            return redirect('register')

    else:
        form = UserCreationForm()
        return render(request, "authenticate/register.html", {'form': form})

def login_user(request):
    if request.method == "POST":
        user_username = request.POST["username"]
        user_password = request.POST["password"]
        user = authenticate(request, username=user_username, password=user_password)
        if user is not None:
            login(request, user)
            curr_user = request.user
            messages.success(request, ("You have been logged in succesfully!!"))
            return redirect("main-page", user_id=curr_user.id)
        else:
            messages.success(request, ("There was an error!"))
            return redirect("login")

    else:
        return render(request, "authenticate/log-in.html")
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been succesfully logged out!"))
    return redirect("home")
    
def show_main_page(request, user_id):
    user_playlists = Playlist.objects.filter(user__pk=user_id).all()

    context = {
        "user_playlists": user_playlists,
    }

    return render(request, "main-page.html", context)