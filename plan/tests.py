from django.test import TestCase

# Create your tests here.
class PlanTestCase(TestCase):

    def test_index(self):
        resp = self.client.get('/roadmap/')
        self.assertEqual(resp.status_code, 200)