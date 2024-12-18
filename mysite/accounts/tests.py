from django.test import TestCase
from accounts.models import AppUser
from django.urls import reverse_lazy


class TestUserCreation(TestCase):

    def test_get_correct_template(self):

        response = self.client.get(reverse_lazy("register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertContains(response, "form")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_correct_user_creation(self):

        form_data = {
            "email": "pesho@pesho.bg",
            "username": "GeorgiGogo",
            "password1": "12admin34",
            "password2": "12admin34",
        }

        response = self.client.post(reverse_lazy("register"), data=form_data)

        self.assertEqual(AppUser.objects.count(), 1)
        self.assertEqual(AppUser.objects.first().username, "GeorgiGogo")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("main-page"))

    def test_incorrect_user_creation(self):

        form_data = {
            "email": "",
            "username": "Gosho",
            "password1": "12admin34",
            "password2": "12admin34",
        }

        response = self.client.post(reverse_lazy("register"), data=form_data)

        self.assertEqual(AppUser.objects.count(), 0)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertContains(response, "This field is required")


class TestUserLogin(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        cls.user = AppUser.objects.create_user(
            email="pesho@pesho.com",
            username="PeshoGotin",
            password="12admin34",
        )

    def test_correct_login(self):

        response = self.client.post(reverse_lazy("login"), {
            "username": "PeshoGotin",
            "password": "12admin34",
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("main-page"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_incorrect_login(self):

        response = self.client.post(reverse_lazy("login"), {
            "username": "Wrong User",
            "password": "Wrong User Password"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_blank_login(self):

        response = self.client.post(reverse_lazy("login"), {
            "username": "",
            "password": "",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertFalse(response.wsgi_request.user.is_authenticated)