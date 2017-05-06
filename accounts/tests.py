from django.test import TestCase

from django.core.urlresolvers import reverse

class AccountViewTests(TestCase):

    def test_accounts_view(self):
        response = self.client.get(reverse('profile_form'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_view(self):
        response = self.client.get(reverse('anonymous_profile'))
        self.assertEqual(response.status_code, 200)

    def test_save_view(self):
        response = self.client.get(reverse('save_error'))
        self.assertEqual(response.status_code, 200)

    def test_major_view(self):
        response = self.client.get(reverse('suggest_major'))
        self.assertEqual(response.status_code, 200)