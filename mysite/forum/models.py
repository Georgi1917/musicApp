from django.db import models
from django.contrib.auth.models import User
from forum.mixins import CommentAndPostMixIn


class ForumPost(CommentAndPostMixIn):
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="forums")
    title = models.CharField(
        null=False,
        blank=False,
        max_length=80
    )

    def get_comment_count(self):

        return self.post_comments.count()
    
    def get_like_count(self):

        return self.post_likes.count()
    
    class Meta:

        ordering = ["-created_at"]


class CommentPost(CommentAndPostMixIn):
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(to=ForumPost, on_delete=models.CASCADE, related_name="post_comments")

    def get_like_count(self):

        return self.comment_likes.count()


class LikePost(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(to=ForumPost, on_delete=models.CASCADE, related_name="post_likes")


class LikeComment(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="liked_comments")
    comment = models.ForeignKey(to=CommentPost, on_delete=models.CASCADE, related_name="comment_likes")