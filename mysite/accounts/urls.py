from django.urls import path
from accounts.views import login_user, register_user, logout_user

urlpatterns = [
    path('log-in-page', login_user, name="login"),
    path('register-page', register_user, name="register"),
    path('logout_user', logout_user, name="logout"),
]