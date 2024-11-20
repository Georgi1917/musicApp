from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from accounts.forms import EditUserForm, PasswordConfirmationForm, LoginUserForm, RegisterUserForm

# Create your views here.


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been registered succesfully!!"))
            return redirect('main-page')

    else:
        form = RegisterUserForm()

    context = {
        "form": form
    }
        
    return render(request, "accounts/register.html", context)
    
def login_user(request):
    if request.method == "POST":
        login_form = LoginUserForm(request=request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, ("You have been logged in succesfully!!"))
            return redirect("main-page")

    else:
        login_form = LoginUserForm()

    context = {
        "login_form": login_form
    }

    return render(request, "accounts/log-in.html", context)
    
def logout_user(request):

    if request.method == "POST":
        
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

            for album in request.user.playlist_set.all():
                
                for song in album.song_set.all():
                    song.delete()
                
                album.delete()

            request.user.delete()

            messages.success(request, "Your account has been succesfully deleted.")

            return redirect("home")

    else:
        form = PasswordConfirmationForm()

    context = {
        "form": form
    }

    return render(request, "accounts/delete-account.html", context)