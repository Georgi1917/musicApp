from django import forms

class SearchForm(forms.Form):
    searched_user = forms.CharField(
        required=False,
        max_length=80,
        label=""
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["searched_user"].widget.attrs["placeholder"] = "Search For Friends"
