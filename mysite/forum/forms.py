from django import forms
from forum.models import ForumPost, CommentPost


class BaseForumForm(forms.ModelForm):

    class Meta:
        model = ForumPost
        fields = ["title", "content"]


class BaseCommentForm(forms.ModelForm):

    class Meta:
        model = CommentPost
        fields = ["content"]


class ForumCreationForm(BaseForumForm):

    pass


class ForumEditForm(BaseForumForm):

    pass


class ForumDeleteForm(BaseForumForm):

    pass


class CommentCreationForm(BaseCommentForm):

    pass


class CommentEditForm(BaseCommentForm):

    pass