from django.test import SimpleTestCase
from django.urls import reverse


class SnacksTests():
    def test_home_page_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)




# Create your tests here.
