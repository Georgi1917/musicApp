from django.db import models
from django.contrib.auth.models import User
from forum.mixins import CreatedUpdatedAtMixIn, UpvotesContentMixIn


class ForumPost(CreatedUpdatedAtMixIn, UpvotesContentMixIn):
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="forums")
    title = models.CharField(
        null=False,
        blank=False,
        max_length=80
    )
    number_of_comments = models.IntegerField(
        default=0
    )


class CommentPost(CreatedUpdatedAtMixIn, UpvotesContentMixIn):
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(to=ForumPost, on_delete=models.CASCADE, related_name="post_comments")


class LikePost(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(to=ForumPost, on_delete=models.CASCADE, related_name="post_likes")


class LikeComment(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="liked_comments")
    comment = models.ForeignKey(to=CommentPost, on_delete=models.CASCADE, related_name="comment_likes")