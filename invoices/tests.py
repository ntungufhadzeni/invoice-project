from django.test import TestCase
from django.urls import reverse


class InvoiceTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_login_url_by_name(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)
