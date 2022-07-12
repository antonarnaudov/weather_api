from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


class BaseApiTests(TestCase):
    """Used instead of TestCase, performs login and creates user session"""
    password = 'mypassword'
    user = {}

    @classmethod
    def setUpTestData(cls):
        """Creates superuser for the tests"""
        cls.user = User.objects.create_superuser('testuser', 'test@test.com', cls.password)
        cls.user.save()

    def setUp(self):
        """Performs login and creates session for the test class"""
        self.client = APIClient()
        self.client.login(username=self.user.username, password=self.password)

        token_url = reverse('login')
        login_data = {
            "username": self.user.username,
            "password": self.password
        }

        token = self.client.post(token_url, login_data, format='json')
        self.client.credentials(Authorization="Bearer " + token.data["access"])
