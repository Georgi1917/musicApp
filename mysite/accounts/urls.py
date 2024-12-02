from django.urls import path
from accounts import views

urlpatterns = [
    path('log-in-page/', views.login_user, name="login"),
    path('register-page/', views.register_user, name="register"),
    path('logout_user/', views.logout_user, name="logout"),
    path('profile-details/', views.account_details, name="account-details"),
    path('edit-profile/', views.edit_account_page, name="edit-account"),
    path('change-password/', views.change_account_password, name="change-password"),
    path('delete-account/', views.delete_account, name="delete-account")
]