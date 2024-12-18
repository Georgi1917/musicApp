from django.urls import path, include
from contacts import views

urlpatterns = [
    path('', views.show_contacts_page, name="contacts-page"),
    path('error/', views.ContactErrorPage.as_view(), name="contacts-error"),
    path('success/', views.ContactsSuccessPage.as_view(), name="contacts-success")
]