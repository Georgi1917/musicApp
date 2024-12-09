from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import Profile
from django.contrib.auth import get_user_model
from accounts.validators import validate_name, validate_email
from accounts.utils import append_validators, remove_help_text
from django.contrib.auth.hashers import check_password

UserModel = get_user_model()

class BaseUserForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=150,
        required=False,
        validators=[validate_name, ]
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        validators=[validate_name, ]
    )

    birthday = forms.DateField(
        required=False
    )

    profile_picture = forms.ImageField(
        required=False
    )

    class Meta:
        model = UserModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BaseUserForm, self).__init__(*args, **kwargs)
        remove_help_text(self)


class LoginUserForm(AuthenticationForm):

    pass


class RegisterUserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ["email", "username"]


class EditUserForm(BaseUserForm):

    class Meta(BaseUserForm.Meta):
        fields = ["email", "username"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        profile = Profile.objects.get(user=instance)

        profile.first_name = self.cleaned_data["first_name"]
        profile.last_name = self.cleaned_data["last_name"]
        profile.birthday = self.cleaned_data["birthday"]
        profile.profile_picture = self.cleaned_data["profile_picture"]

        if "profile_picture-clear" in self.data:
            profile.profile_picture = None

        if commit:
            instance.save()
            profile.save()

        return instance


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


        