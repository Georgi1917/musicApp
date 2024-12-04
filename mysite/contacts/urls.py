from django.urls import path, include
from contacts import views

urlpatterns = [
    path('', views.show_contacts_page, name="contacts-page")
]