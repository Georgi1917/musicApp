from forum.models import ForumPost
from django.db.models import Count

def get_queryset(filter_by):

    if not filter_by or filter_by == "Newest":

        return ForumPost.objects.all()
    
    if filter_by == "Oldest":

        return ForumPost.objects.all().order_by("created_at")
    
    if filter_by == "Most Liked":

        return ForumPost.objects.annotate(like_count=Count("post_likes")).order_by("-like_count")
    
    if filter_by == "Least Liked":

        return ForumPost.objects.annotate(like_count=Count("post_likes")).order_by("like_count")