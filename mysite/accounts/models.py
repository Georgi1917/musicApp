from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from accounts.managers import CustomUserManager


class AppUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            "unique": "A user with that username already exists."
        }
    )

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "A user with that email already exists."
        }
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):

        return self.username
    
    def delete(self, *args, **kwargs):
        self.profile.profile_picture.delete(save=False)
        super().delete(*args, **kwargs)
    

class Profile(models.Model):

    user = models.OneToOneField(to=AppUser, on_delete=models.CASCADE, related_name="profile")

    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        height_field=None, width_field=None, 
        max_length=100,
        blank=True,
        null=True,
    )

    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    birthday = models.DateField(
        null=True,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
    )

    def get_playlist_count(self):

        return self.user.playlists.count()
    
    def get_songs_count(self):

        song_count = 0

        for playlist in self.user.playlists.all():

            song_count += playlist.songs.count()

        return song_count
    
    def get_posts_count(self):

        return self.user.forums.count()
    
    def get_comments_count(self):

        return self.user.comments.count()
    
    def save(self, *args, **kwargs):

        if self.pk:
            old_instance = Profile.objects.filter(id=self.pk).first()

            if old_instance and old_instance.profile_picture:
                old_instance.profile_picture.delete(save=False)

        base_slug = slugify(self.user.username)

        self.slug = base_slug

        super().save(*args, **kwargs)

    def __str__(self):

        return self.first_name + " " + self.last_name