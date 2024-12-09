from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from forum.helpers import get_queryset
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from forum.models import ForumPost, CommentPost, LikePost, LikeComment
from forum.forms import ForumCreationForm, CommentCreationForm, ForumEditForm, CommentEditForm, FilterPostsForm, SearchPostForm
from rest_framework.response import Response
from rest_framework.decorators import api_view


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_forum_page(request):

    search_form = SearchPostForm()
    form = FilterPostsForm()

    filter_by = request.GET.get("filter_by", "Newest")
    searched_post = request.GET.get("searched_post", "")

    queryset = get_queryset(filter_by)

    queryset = queryset.filter(title__icontains=searched_post)

    paginator = Paginator(queryset, 5)

    page_num = request.GET.get("page", 1)

    page_object = paginator.get_page(page_num)

    form.initial["filter_by"] = filter_by
    search_form.initial["searched_post"] = searched_post

    context = {
        "posts": page_object,
        "likes": list(map(lambda x: x.post, request.user.likes.all())),
        "form": form,
        "search_form": search_form,
        "filter_by": filter_by,
        "searched_post": searched_post,
        "page_num": page_num,
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
        "likes": request.user.likes.filter(post_id=post_id),
        "liked_comments": list(map(lambda x: x.comment, request.user.liked_comments.all())),
        "ref": request.GET.get("ref", "all_posts"),
        "searched_post": request.GET.get("searched_post"),
        "filter_by": request.GET.get("filter_by", "Newest"),
        "page_num": request.GET.get("page")
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

            comment.save()

            return redirect(f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref")}")

    context ={
        "form": form
    }

    return render(request, "forum/create-comment.html", context)


def delete_comment(request, post_id, comment_id):

    comment = request.user.comments.filter(id=comment_id).first()

    if comment:
    
        comment.delete()
    
    if request.GET.get("ref") == "user_comments":
        
        return redirect('profile-comments')

    else:

        return redirect(f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref")}")


def delete_post(request, post_id):

    post = request.user.forums.filter(id=post_id).first()

    if post:

        post.delete()

    if request.GET.get("ref") == "user_posts":

        return redirect('profile-posts')
    
    else:

        return redirect('forum')


def edit_post(request, post_id):
    
    form = ForumEditForm(instance=request.user.forums.get(id=post_id))

    if request.method == "POST":

        form = ForumCreationForm(request.POST, instance=request.user.forums.get(id=post_id))

        if form.is_valid():

            form.save()

            return redirect(f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref")}")
            
    context = {
        "form": form
    }

    return render(request, "forum/edit-post.html", context)


def edit_comment(request, post_id, comment_id):

    form = CommentEditForm(instance=request.user.comments.get(id=comment_id))

    if request.method == "POST":

        form = CommentEditForm(request.POST, instance=request.user.comments.get(id=comment_id))

        if form.is_valid():

            form.save()

            if request.GET.get("ref") == "user_comments":

                return redirect('profile-comments')

            else:

                return redirect(f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref")}")

    context = {
        "form": form
    }

    return render(request, "forum/edit-comment.html", context)


@api_view(["GET"])
def like_post(request, post_id):

    post = ForumPost.objects.get(id=post_id)
    like = LikePost.objects.filter(post=post, user=request.user).first()
    status = "liked"

    if like:

        like.delete()
        status = "unliked"

    else:

        LikePost.objects.create(
            post=post, 
            user=request.user
        )

    return Response({
        "status": status,
        "likes_count": post.post_likes.count()
    })


@api_view(["GET"])
def like_comment(request, post_id, comment_id):
    
    comment = CommentPost.objects.get(id=comment_id)
    like = LikeComment.objects.filter(user=request.user, comment=comment)
    status = "liked"

    if like:

        like.delete()
        status = "unliked"

    else:

        LikeComment.objects.create(
            user=request.user,
            comment=comment
        )

    return Response({
        "status": status,
        "likes_count": comment.comment_likes.count()
    })