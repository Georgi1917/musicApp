from django.shortcuts import render, redirect
from forum.models import ForumPost, CommentPost, LikePost
from forum.forms import ForumCreationForm, CommentCreationForm
from rest_framework.response import Response
from rest_framework.decorators import api_view


def show_forum_page(request):

    context = {
        "posts": ForumPost.objects.all(),
        "likes": list(map(lambda x: x.post, request.user.likes.all()))
    }

    return render(request, "forum/forums-page.html", context)


def show_forum_create_page(request):

    form = ForumCreationForm(request.POST or None)

    if request.method == "POST":
        
        if form.is_valid():

            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('forum')

    context = {
        "form": form
    }

    return render(request, "forum/forum-create-page.html", context)


def show_post(request, post_id):

    context = {
        "post": ForumPost.objects.get(id=post_id),
        "comments": CommentPost.objects.filter(post_id=post_id),
        "likes": request.user.likes.filter(post_id=post_id)
    }

    return render(request, "forum/post-page.html", context)


def create_comment(request, post_id):

    form = CommentCreationForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            post = ForumPost.objects.get(id=post_id)

            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            post.number_of_comments += 1

            post.save()
            comment.save()

            return redirect('show-post', post_id=post_id)

    context ={
        "form": form
    }

    return render(request, "forum/create-comment.html", context)


def delete_comment(request, post_id, comment_id):

    comment = CommentPost.objects.get(id=comment_id)
    post = ForumPost.objects.get(id=post_id)

    post.number_of_comments -= 1

    post.save()
    comment.delete()

    return redirect('show-post', post_id=post_id)


def delete_post(request, post_id):

    post = request.user.forums.filter(id=post_id).first()

    if post:

        post.delete()

    return redirect('forum')


@api_view(["GET"])
def like_post(request, post_id):

    post = ForumPost.objects.get(id=post_id)
    like = LikePost.objects.filter(post=post, user=request.user).first()

    if like:
        like.delete()
        post.upvotes = post.post_likes.count()
        post.save()

        response_data = {
            "status": "unliked",
            "likes_count": post.upvotes
        }

        return Response(response_data)
    
    LikePost.objects.create(post=post, user=request.user)
    post.upvotes = post.post_likes.count()
    post.save()

    response_data = {
            "status": "liked",
            "likes_count": post.upvotes
    }

    return Response(response_data)