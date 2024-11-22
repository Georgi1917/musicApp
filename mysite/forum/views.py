from django.shortcuts import render, redirect
from forum.models import ForumPost, CommentPost
from forum.forms import ForumCreationForm, CommentCreationForm


def show_forum_page(request):

    all_forum_posts = ForumPost.objects.all()

    context = {
        "posts": all_forum_posts,
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
    post = ForumPost.objects.get(id=post_id)

    comments = CommentPost.objects.filter(post=post)

    context = {
        "post": post,
        "comments": comments,
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