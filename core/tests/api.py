from rest_framework import status
from rest_framework.reverse import reverse

from core.tests.base import BaseApiTests


class TestUser(BaseApiTests):
    """Tests User API"""
    password = 'newPassword2'
    email = 'newuser@example.com'

    def test_get_user_detailed(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_register_new_user(self):
        data = {'username': 'newuser', 'email': self.email, 'password': self.password, 'password2': self.password}

        url = reverse('user-list')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(response.data['user']['email'], self.email)

    def test_register_no_username(self):
        data = {'email': self.email, 'password': self.password, 'password2': self.password}

        url = reverse('user-list')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
