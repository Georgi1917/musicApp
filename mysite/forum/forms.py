from django import forms
from forum.models import ForumPost, CommentPost

class ForumCreationForm(forms.ModelForm):

    class Meta:
        model = ForumPost
        fields = ["title", "content", "hide_upvotes"]


class CommentCreationForm(forms.ModelForm):

    class Meta:
        model = CommentPost
        fields = ["content", "hide_upvotes"]