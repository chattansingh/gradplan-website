from django.test import TestCase

from django.core.urlresolvers import reverse

class professorratingviewTests(TestCase):
    def test_addrating_view(self):
        response = self.client.get(reverse('addrating'))
        self.assertEqual(response.status_code, 200)
    def test_accounts_view(self):
        response = self.client.get(reverse('youshouldntbehere'))
        self.assertEqual(response.status_code, 200)
