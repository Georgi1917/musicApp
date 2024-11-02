from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.validators import validate_name

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=45)
    password = forms.CharField(required=True, max_length=30, widget=forms.PasswordInput)

class BaseUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BaseUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ""
        self.fields["first_name"].validators.append(validate_name)
        self.fields["last_name"].validators.append(validate_name)


class EditUserForm(BaseUserForm):

    class Meta(BaseUserForm.Meta):
        fields = ["email", "username", "first_name", "last_name"]