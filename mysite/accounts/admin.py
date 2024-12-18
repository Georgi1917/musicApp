from django.contrib import admin
from accounts.models import AppUser, Profile
from accounts.forms import CustomUserAddForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

UserModel = get_user_model()

@admin.register(UserModel)
class AppUserAdmin(UserAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserAddForm

    list_display = ("username", "email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email")
    fieldsets = ()

    search_fields = ("username", "email")
    list_filter = ("is_superuser", "is_staff")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    pass