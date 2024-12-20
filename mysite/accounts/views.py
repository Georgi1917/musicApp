from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from accounts.forms import EditUserForm, PasswordConfirmationForm, LoginUserForm, RegisterUserForm
from django.views.decorators.cache import cache_control
from django.conf import settings


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
            next_url = request.GET.get("next", "")

            if not next_url:

                return redirect("main-page")

            return redirect(next_url)

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
        return redirect("main-page")


@login_required(login_url=settings.LOGIN_URL)
def account_details(request):

    context = {
        "app_user": request.user
    }

    return render(request, "accounts/profile-details.html", context)


@login_required(login_url=settings.LOGIN_URL)
def edit_account_page(request):

    if request.method == "POST":
        user_form = EditUserForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            return redirect("account-details")

    else:

        user_profile = request.user.profile

        initial_data = {
            "email": request.user.email,
            "username": request.user.username,
            "first_name": user_profile.first_name,
            "last_name": user_profile.last_name,
            "birthday": user_profile.birthday,
            "profile_picture": user_profile.profile_picture
        }

        user_form = EditUserForm(initial=initial_data)

    context = {
        "form": user_form
    }

    return render(request, "accounts/edit-account.html", context)


@login_required(login_url=settings.LOGIN_URL)
def change_account_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            return redirect("account-details")

    else:

        form = PasswordChangeForm(request.user)

    context = {
        "form": form
    }

    return render(request, "accounts/change-password.html", context)


@login_required(login_url=settings.LOGIN_URL)
def delete_account(request):

    if request.method == "POST":
        form = PasswordConfirmationForm(request.POST, request.user)

        if form.is_valid():

            for album in request.user.playlists.all():
                
                for song in album.songs.all():
                    song.delete()
                
                album.delete()

            request.user.delete()

            messages.success(request, "Your account has been succesfully deleted.")

            return redirect("main-page")

    else:
        form = PasswordConfirmationForm()

    context = {
        "form": form
    }

    return render(request, "accounts/delete-account.html", context)


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_posts(request):

    context = {
        "posts": request.user.forums.all(),
        "likes": list(map(lambda x: x.post, request.user.likes.all()))
    }

    return render(request, "accounts/profile-posts.html", context)


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_comments(request):

    context = {
        "comments": request.user.comments.all(),
        "liked_comments": list(map(lambda x: x.comment, request.user.liked_comments.all()))
    }

    return render(request, "accounts/profile-comments.html", context)