from django.contrib import admin
from forum.models import ForumPost, CommentPost


class CommentInline(admin.TabularInline):

    model = CommentPost
    fields = ("user", "content")
    extra = 1


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):

    ordering = ("-created_at", )
    search_fields = ("title", "content")
    inlines = (CommentInline, )


@admin.register(CommentPost)
class CommentPostAdmin(admin.ModelAdmin):

    ordering = ("-created_at", )
    search_fields = ("content", )
