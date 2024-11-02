from django.urls import path
from accounts.views import login_user, register_user, logout_user, edit_account_page

urlpatterns = [
    path('log-in-page/', login_user, name="login"),
    path('register-page/', register_user, name="register"),
    path('logout_user/', logout_user, name="logout"),
    path('edit-profile/', edit_account_page, name="edit-account")
]