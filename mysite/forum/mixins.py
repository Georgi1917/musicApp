from django.db import models


class UpvotesContentMixIn(models.Model):

    content = models.TextField(
        null=False,
        blank=False
    )
    upvotes = models.IntegerField(
        default=0
    )

    class Meta:
        abstract = True


class CreatedUpdatedAtMixIn(models.Model):
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        abstract = True