from django import forms


class ContactForm(forms.Form):

    from_ = forms.EmailField(
        label="From ",
        required=True
    )
    subject = forms.CharField(
        max_length=100,
    )
    content = forms.CharField(
        widget=forms.Textarea,
        label="Message "
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["from_"].disabled = True