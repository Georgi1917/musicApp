from django.urls import path
from album_creation.views import show_album_creation_page, show_album_edit_page

urlpatterns = [
    path('create-album/', show_album_creation_page, name="album"),
    path('edit-album/<int:album_id>/', show_album_edit_page, name="edit_album"),
]