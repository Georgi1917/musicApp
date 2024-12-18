from django.db import models
from django.contrib.auth import get_user_model
from forum.mixins import CommentAndPostMixIn

UserModel = get_user_model()

class ForumPost(CommentAndPostMixIn):
    
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="forums")
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

    def __str__(self):

        return self.title


class CommentPost(CommentAndPostMixIn):
    
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(to=ForumPost, on_delete=models.CASCADE, related_name="post_comments")

    def get_like_count(self):

        return self.comment_likes.count()
    
    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return f"{self.user} - {self.post} - Comment - {self.pk}"


class LikePost(models.Model):

    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(to=ForumPost, on_delete=models.CASCADE, related_name="post_likes")


class LikeComment(models.Model):

    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="liked_comments")
    comment = models.ForeignKey(to=CommentPost, on_delete=models.CASCADE, related_name="comment_likes")