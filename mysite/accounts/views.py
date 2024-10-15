from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

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
            return redirect('main-page', user_id=curr_user.id)
        else:
            messages.success(request, ("There was an error, please try again!"))
            return redirect('register')

    else:
        form = UserCreationForm()
        return render(request, "accounts/register.html", {'form': form})
    
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
        return render(request, "accounts/log-in.html")
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been succesfully logged out!"))
    return redirect("home")