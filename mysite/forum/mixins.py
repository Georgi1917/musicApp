from django.db import models


class CommentAndPostMixIn(models.Model):
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    content = models.TextField(
        null=False,
        blank=False
    )

    class Meta:

        abstract = True