from django.urls import path, include
from forum import views

urlpatterns = [
    # path('forum-page/', views.show_forum_page, name="forum"),
    # path('create-forum/', views.show_forum_create_page, name="create-forum")
    path('forum-page/', include([
        path('', views.show_forum_page, name="forum"),
        path('create-post/', views.show_forum_create_page, name="create-post"),
        path('post/<int:post_id>/', views.show_post, name="show-post"),
        path('post/<int:post_id>/like/', views.like_post, name="like-post"),
        path('post/<int:post_id>/delete/', views.delete_post, name="delete-post"),
        path('post/<int:post_id>/create-comment/', views.create_comment, name="create-comment"),
        path('post/<int:post_id>/delete-comment/<int:comment_id>/', views.delete_comment, name="delete-comment")
    ]))
]