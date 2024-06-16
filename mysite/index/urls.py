from django.urls import path
from index.views import home_page_index, login_user, register_user, show_main_page, logout_user

urlpatterns = [
    path('', home_page_index, name="home"),
    path('log-in-page', login_user, name="login"),
    path('register-page', register_user, name="register"),
    path('main-page/<int:user_id>', show_main_page, name="main-page"),
    path('logout_user', logout_user, name="logout")
]