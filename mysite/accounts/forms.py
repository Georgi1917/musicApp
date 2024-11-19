from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from accounts.validators import validate_name
from accounts.utils import append_validators, remove_help_text
from django.contrib.auth.hashers import check_password

class BaseUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BaseUserForm, self).__init__(*args, **kwargs)
        remove_help_text(self)
        append_validators(self, ["first_name", "last_name"], validate_name)


class LoginUserForm(AuthenticationForm):

    pass


class EditUserForm(BaseUserForm):

    class Meta(BaseUserForm.Meta):
        fields = ["email", "username", "first_name", "last_name"]


class PasswordConfirmationForm(forms.Form):
    password1 = forms.CharField(
        required=True,
        label="Enter your Password:",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        required=True,
        label="Confirm Password:",
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:

            if password1 != password2:
                raise ValidationError("The passwords do not match!")
            
            if self.user and not self.user.check_password(password1):
                raise ValidationError("Invalid Password!")
            
        return cleaned_data


        