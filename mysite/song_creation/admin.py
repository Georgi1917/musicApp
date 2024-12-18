from django.contrib import admin
from song_creation.models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):

    search_fields = ("name", "author")