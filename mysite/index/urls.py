from django.urls import path
from index.views import home_page_index, show_main_page

urlpatterns = [
    path('', home_page_index, name="home"),
    path('main-page/', show_main_page, name="main-page"),
]