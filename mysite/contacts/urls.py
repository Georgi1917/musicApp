from django.urls import path, include
from contacts import views

urlpatterns = [
    path('', views.show_contacts_page, name="contacts-page"),
    path('error/', views.show_contacts_error_page, name="contacts-error"),
    path('success/', views.show_contacts_success_page, name="contacts-success")
]