import time
from django.test import TestCase
from django.urls import reverse


class SearchViewTest(TestCase):
    """Тесты для SearchView"""

    def test_view_speed(self):
        start_time = time.time()
        self.client.post(reverse("provider_a:search"))
        end_time = time.time()
        self.assertTrue(end_time - start_time >= 30)
