from django.urls import path
from index.views import MainPage

urlpatterns = [
    path('', MainPage.as_view(), name="main-page"),
]