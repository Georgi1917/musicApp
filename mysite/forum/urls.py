from django.urls import path, include
from forum import views

urlpatterns = [
    path('forum-page/', include([
        path('', views.show_forum_page, name="forum"),
        path('create-post/', views.CreateForumPost.as_view(), name="create-post"),
        path('post/<int:post_id>/', include([
            path('', views.show_post, name="show-post"),
            path('like/', views.like_post, name="like-post"),
            path('like/<int:comment_id>/', views.like_comment, name="like-comment"),
            path('edit-post/', views.edit_post, name="edit-post"),
            path('edit-comment/<int:comment_id>/', views.edit_comment, name="edit-comment"), 
            path('delete-post/', views.delete_post, name="delete-post"),
            path('create-comment/', views.create_comment, name="create-comment"),
            path('delete-comment/<int:comment_id>/', views.delete_comment, name="delete-comment")
        ]))
    ]))
]