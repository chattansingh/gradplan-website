from django.test import TestCase

# Create your tests here.
from django.core.urlresolvers import reverse

class planTestS(TestCase):

    def Test_plans(self):
        response = self.client.get(reverse('Plans'))
        self.assertEqual(response.status_code,200)

    def Test_choose_major(self):
        response = self.client.get(reverse('choose_major'))
        self.assertEqual(response.status_code, 200)

    def Test_choose_semester(self):
        response = self.client.get(reverse('choose_semester'))
        self.assertEqual(response.status_code, 200)

    def Test_graduation_roadmap(self):
        response = self.client.get(reverse('graduation_roadmap'))
        self.assertEqual(response.status_code, 200)

    def Test_job_information(self):
        response = self.client.get(reverse('job_information'))
        self.assertEqual(response.status_code, 200)

    def Test_modify_plan(self):
        response = self.client.get(reverse('modify_plan'))
        self.assertEqual(response.status_code, 200)

    def Test_newplan(self):
        response = self.client.get(reverse('newPlan'))
        self.assertEqual(response.status_code, 200)

    def Test_test(self):
        response = self.client.get(reverse('test'))
        self.assertEqual(response.status_code, 200)



