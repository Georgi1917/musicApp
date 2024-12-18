from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import get_object_or_404
from forum.helpers import get_queryset
from django.views.decorators.cache import cache_control
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
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

    paginator = Paginator(queryset, 10)

    page_num = request.GET.get("page", 1)

    page_object = paginator.get_page(page_num)

    form.initial["filter_by"] = filter_by
    search_form.initial["searched_post"] = searched_post

    if request.user.is_authenticated:

        likes = list(map(lambda x: x.post, request.user.likes.all()))
    
    else:

        likes = []

    context = {
        "posts": page_object,
        "likes": likes,
        "form": form,
        "search_form": search_form,
        "filter_by": filter_by,
        "searched_post": searched_post,
        "page_num": page_num,
    }
    
    return render(request, "forum/forums-page.html", context)


class CreateForumPost(LoginRequiredMixin, CreateView):

    model = ForumPost
    form_class = ForumCreationForm
    template_name = "forum/forum-create-page.html"
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy("forum")

    def form_valid(self, form):

        form.instance.user = self.request.user

        return super().form_valid(form)



def show_post(request, post_id):

    if request.user.is_authenticated:

        likes = request.user.likes.filter(post_id=post_id)
        liked_comments = list(map(lambda x: x.comment, request.user.liked_comments.all()))

    else:

        likes = []
        liked_comments = []

    context = {
        "post": get_object_or_404(ForumPost, id=post_id),
        "comments": CommentPost.objects.filter(post_id=post_id),
        "likes": likes,
        "liked_comments": liked_comments,
        "ref": request.GET.get("ref", "all_posts"),
        "friend_slug": request.GET.get("friend_slug", ""),
        "searched_post": request.GET.get("searched_post", ""),
        "filter_by": request.GET.get("filter_by", "Newest"),
        "page_num": request.GET.get("page", 1)
    }

    return render(request, "forum/post-page.html", context)


@login_required(login_url=settings.LOGIN_URL)
def create_comment(request, post_id):

    form = CommentCreationForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            post = get_object_or_404(ForumPost, id=post_id)

            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post

            comment.save()

            if request.GET.get("ref") == "user_posts" or request.GET.get("ref") == "user_comments":
                
                return redirect(f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref", "user_posts")}")
            
            elif request.GET.get("ref") == "friend_posts":

                return redirect(
                    f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref", "friend_posts")}&friend_slug={request.GET.get("friend_slug", "")}"
                )
            
            else:

                return redirect(
                    f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?searched_post={request.GET.get("searched_post", "")}&filter_by={request.GET.get("filter_by", "Newest")}&page={request.GET.get("page", 1)}&ref={request.GET.get("ref", "all_posts")}"
                )

    context ={
        "form": form
    }

    return render(request, "forum/create-comment.html", context)


@login_required(login_url=settings.LOGIN_URL)
def delete_comment(request, post_id, comment_id):

    try:

        comment = request.user.comments.get(id=comment_id)

    except ObjectDoesNotExist:

        raise Http404

    comment.delete()
    
    if request.GET.get("ref") == "user_comments":
        
        return redirect('profile-comments')
    
    elif request.GET.get("ref") == "user_posts":

        return redirect(
            f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref", "user_posts")}"
        )
    
    elif request.GET.get("ref") == "friend_posts":

        return redirect(
            f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref", "friend_posts")}&friend_slug={request.GET.get("friend_slug", "")}"
        )

    else:

        return redirect(
            f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?searched_post={request.GET.get("searched_post", "")}&filter_by={request.GET.get("filter_by", "Newest")}&page={request.GET.get("page", 1)}&ref={request.GET.get("ref", "all_posts")}"
        )


@login_required(login_url=settings.LOGIN_URL)
def delete_post(request, post_id):

    try:

        post = request.user.forums.get(id=post_id)

    except ObjectDoesNotExist:

        raise Http404

    post.delete()

    if request.GET.get("ref") == "user_comments":

        return redirect('profile-comments')

    elif request.GET.get("ref") == "user_posts":

        return redirect('profile-posts')
    
    else:

        return redirect('forum')


@login_required(login_url=settings.LOGIN_URL)
def edit_post(request, post_id):
    
    try:

        form = ForumEditForm(instance=request.user.forums.get(id=post_id))

    except ObjectDoesNotExist:

        raise Http404

    if request.method == "POST":

        form = ForumCreationForm(request.POST, instance=request.user.forums.get(id=post_id))

        if form.is_valid():

            form.save()

            if request.GET.get("ref") == "user_posts" or request.GET.get("ref") == "user_comments":

                return redirect(f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref")}")

            else:

                return redirect(
                    f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?searched_post={request.GET.get("searched_post", "")}&filter_by={request.GET.get("filter_by", "Newest")}&page={request.GET.get("page", 1)}&ref={request.GET.get("ref")}"
                )
            
    context = {
        "form": form
    }

    return render(request, "forum/edit-post.html", context)


@login_required(login_url=settings.LOGIN_URL)
def edit_comment(request, post_id, comment_id):

    try:

        form = CommentEditForm(instance=request.user.comments.get(id=comment_id))

    except ObjectDoesNotExist:

        raise Http404

    if request.method == "POST":

        form = CommentEditForm(request.POST, instance=request.user.comments.get(id=comment_id))

        if form.is_valid():

            form.save()

            if request.GET.get("ref") == "user_comments":

                return redirect('profile-comments')
            
            elif request.GET.get("ref") == "user_posts":

                return redirect(f"{reverse_lazy("show-post", kwargs={"post_id": post_id})}?ref={request.GET.get("ref", "user_posts")}")
            
            elif request.GET.get("ref") == "friend_posts":

                return redirect(f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?ref={request.GET.get("ref", "friend_posts")}&friend_slug={request.GET.get("friend_slug", "")}")

            else:

                return redirect(f"{reverse_lazy('show-post', kwargs={"post_id": post_id})}?searched_post={request.GET.get("searched_post", "")}&filter_by={request.GET.get("filter_by", "Newest")}&page={request.GET.get("page", 1)}&ref={request.GET.get("ref")}")

    context = {
        "form": form
    }

    return render(request, "forum/edit-comment.html", context)


@api_view(["GET"])
def like_post(request, post_id):

    if not request.user.is_authenticated:

        return Response({
            "status": 403,
            "redirect_url": f"{reverse_lazy("login")}?next={reverse_lazy("forum")}"
        })

    post = get_object_or_404(ForumPost, id=post_id)
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

    if not request.user.is_authenticated:

        return Response({
            "status": 403,
            "redirect_url": f"{reverse_lazy("login")}?next={reverse_lazy("forum")}"
        })
    
    comment = get_object_or_404(CommentPost, id=comment_id)
    like = LikeComment.objects.filter(user=request.user, comment=comment).first()
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