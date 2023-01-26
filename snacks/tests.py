from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Snack


class SnacksTests(TestCase):
    def set_up(self):
        self.user = get_user_model().objects.create_user(username="tester", email="test@gmail.com", password="pass")

        self.snack = Snack.objects.create(title="popsicle", purchaser=self.user, description="description of popsicle")

    def test_str_representation(self):
        self.assertEqual(str(self.snack), "popsicle")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.name}", "popsicle")
        self.assertEqual(f"{self.snack.purchaser}", "tester")
        self.assertEqual(f"{self.snack.description}", "description of popsicle")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "popsicle")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/500")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Purchaser: tester")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "Cake",
                "purchaser": self.user.id,
                "description": "Yum!"
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Cake")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Updated Title", "purchaser": self.user.id, "description": "test description",}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"), target_status_code=200)

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args=1))
        self.assertEqual(response.status_code, 200)

    def test_model(self):
        snack = Snack.objects.create(title="cookies", purchaser=self.user)
        self.assertEqual(snack.name, "cookies")



