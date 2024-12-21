from django.test import TestCase
from album_creation.models import Playlist, FollowedPlaylist
from accounts.models import AppUser
from django.urls import reverse_lazy


class TestPlaylistPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        cls.user = AppUser.objects.create_user(
            email="pesho@pesho.bg",
            username="PeshoGotin",
            password="12admin34",
        )

        cls.another_user = AppUser.objects.create_user(
            email="ivan@ivanov.bg",
            username="IvanIvanov",
            password="12admin34",
        )

        cls.playlist1 = Playlist.objects.create(
            name="Rock",
            description="A cool rock playlist",
            user=cls.user
        )

        cls.playlist2 = Playlist.objects.create(
            name="Folk",
            description="A cool folk playlist",
            user=cls.user
        )

        cls.playlist3 = Playlist.objects.create(
            name="Regae",
            description="A cool regae playlist",
            user=cls.another_user
        )

        cls.playlist4 = Playlist.objects.create(
            name="Heavy Metal",
            description="A cool Heavy Metal Playlist",
            user=cls.another_user
        )

        cls.followed_playlist1 = FollowedPlaylist.objects.create(
            user=cls.user,
            playlist=cls.playlist3
        )

        cls.followed_playlist2 = FollowedPlaylist.objects.create(
            user=cls.user,
            playlist=cls.playlist4
        )

    def test_playlist_page_not_authenticated_user_status_code(self):

        response = self.client.get(reverse_lazy("playlist-page"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse_lazy("login")}?next={reverse_lazy("playlist-page")}")

    def test_playlist_page_not_authenticated_user_template_user(self):

        response = self.client.get(reverse_lazy("playlist-page"))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "album_creation/playlist.page")
        self.assertRedirects(response, f"{reverse_lazy("login")}?next={reverse_lazy("playlist-page")}")

    def test_playlist_page_authenticated_user_status_code(self):

        self.client.login(username="PeshoGotin", password="12admin34")

        response = self.client.get(reverse_lazy("playlist-page"))
        self.assertEqual(response.status_code, 200)

    def test_playlist_page_authenticated_user_template(self):

        self.client.login(username="PeshoGotin", password="12admin34")

        response = self.client.get(reverse_lazy("playlist-page"))
        self.assertTemplateUsed(response, "album_creation/playlist-page.html")

    def test_playlist_page_context_data(self):

        self.client.login(username="PeshoGotin", password="12admin34")

        response = self.client.get(reverse_lazy("playlist-page"))
        self.assertEqual(list(response.context["user_playlists"]), [self.playlist1, self.playlist2])
        self.assertEqual(list(response.context["followed_playlists"]), [self.followed_playlist1, self.followed_playlist2])


class TestEditPlaylistPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        cls.user = AppUser.objects.create_user(
            email="pesho@pesho.bg",
            username="PeshoGotin",
            password="12admin34",
        )

        cls.playlist = Playlist.objects.create(
            name="Rock",
            description="A cool Rock Playlist",
            user=cls.user
        )

    def setUp(self):
        
        self.client.login(username="PeshoGotin", password="12admin34")

    def test_edit_playlist_page_status_code(self):

        response = self.client.get(reverse_lazy("edit-playlist", kwargs={"album_id": self.playlist.id}))

        self.assertEqual(response.status_code, 200)

    def test_edit_playlist_page_template_used(self):

        response = self.client.get(reverse_lazy("edit-playlist", kwargs={"album_id": self.playlist.id}))

        self.assertTemplateUsed(response, "album_creation/edit_album.html")

    def test_edit_playlist_page_updates_playlist_on_post(self):

        post_data = {
            "name": "Folk",
            "description": "I Love Folk Music!",
        }

        response = self.client.post(reverse_lazy("edit-playlist", kwargs={"album_id": self.playlist.id}), data=post_data)

        self.playlist.refresh_from_db()

        self.assertEqual(self.playlist.name, "Folk")
        self.assertEqual(self.playlist.description, "I Love Folk Music!")

        self.assertRedirects(response, reverse_lazy("playlist-page"))

    def test_edit_playlist_page_404_on_invalid_id(self):

        response = self.client.get(reverse_lazy("edit-playlist", kwargs={"album_id": 100000}))

        self.assertEqual(response.status_code, 404)

    def test_edit_playlist_page_redirects_on_non_logged_in_users(self):

        self.client.logout()

        response = self.client.get(reverse_lazy("edit-playlist", kwargs={"album_id": self.playlist.id}))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "album_creation/edit_album.html")
        self.assertRedirects(response, f"{reverse_lazy("login")}?next={reverse_lazy("edit-playlist", kwargs={"album_id": self.playlist.id})}")