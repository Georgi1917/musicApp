from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from accounts.forms import LoginForm, EditUserForm, PasswordConfirmationForm
from album_song_creation.models import Playlist
from song_creation.models import Song

# Create your views here.


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
            return redirect('main-page')

    else:
        form = UserCreationForm()
        
    return render(request, "accounts/register.html", {'form': form})
    
def login_user(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_username = login_form.cleaned_data["username"]
            user_password = login_form.cleaned_data["password"]
            user = authenticate(request, username=user_username, password=user_password)
            if user is not None:
                login(request, user)
                messages.success(request, ("You have been logged in succesfully!!"))
                return redirect("main-page")

    else:
        login_form = LoginForm()

    context = {
        "login_form": login_form
    }

    return render(request, "accounts/log-in.html", context)
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been succesfully logged out!"))
    return redirect("home")

def edit_account_page(request):

    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            return redirect("main-page")

    else:
        user_form = EditUserForm(instance=request.user)

    context = {
        "form": user_form
    }

    return render(request, "accounts/account-page.html", context)

def change_account_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            return redirect("edit-account")

    else:

        form = PasswordChangeForm(request.user)

    context = {
        "form": form
    }

    return render(request, "accounts/change-password.html", context)

def delete_account(request):

    if request.method == "POST":
        form = PasswordConfirmationForm(request.POST, request.user)

        if form.is_valid():
            
            user = request.user

            user_albums = Playlist.objects.filter(user=user)

            for album in user_albums:
                songs_in_album = Song.objects.filter(album=album)
                for song in songs_in_album:
                    song.delete()
                
                album.delete()

            user.delete() 

            messages.success(request, "Your account has been succesfully deleted.")

            return redirect("home")

    else:
        form = PasswordConfirmationForm()

    context = {
        "form": form
    }

    return render(request, "accounts/delete-account.html", context)