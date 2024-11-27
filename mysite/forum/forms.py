from django import forms
from forum.models import ForumPost, CommentPost


class FilterPostsForm(forms.Form):

    CHOICES = (
        ("Newest", "Newest"),
        ("Oldest", "Oldest"),
        ("Most Liked", "Most Liked"),
        ("Least Liked", "Least Liked")
    )

    filter_by = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        initial="Newest"
    )


class SearchPostForm(forms.Form):

    searched_post = forms.CharField(
        required=False,
        label="",
        max_length=80
    )

    def __init__(self, *args, **kwargs):
        super(SearchPostForm, self).__init__(*args, **kwargs)
        self.fields["searched_post"].widget.attrs["placeholder"] = "Search For Posts"


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


# TODO:
class ForumDeleteForm(BaseForumForm): 

    pass


class CommentCreationForm(BaseCommentForm):

    pass


class CommentEditForm(BaseCommentForm):

    pass


# TODO:
class CommentDeleteForm(BaseCommentForm):

    pass
