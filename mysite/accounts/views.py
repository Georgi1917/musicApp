from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import LoginForm

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
                curr_user = request.user
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