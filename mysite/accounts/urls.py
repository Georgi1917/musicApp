from django.urls import path
from accounts import views

urlpatterns = [
    path('log-in-page/', views.login_user, name="login"),
    path('register-page/', views.register_user, name="register"),
    path('logout_user/', views.logout_user, name="logout"),
    path('profile-details/', views.account_details, name="account-details"),
    path('profile-details/posts/', views.user_posts, name="profile-posts"),
    path('profile-details/comments/', views.user_comments, name="profile-comments"),
    path('edit-profile/', views.edit_account_page, name="edit-account"),
    path('change-password/', views.change_account_password, name="change-password"),
    path('delete-account/', views.delete_account, name="delete-account")
]