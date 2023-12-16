from django.urls import reverse

from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)


class BaseAPITestCase(APITestCase):
    """Written BaseAPITestCase for not repeating the same code in the test"""

    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        payload = {
            "email": "osman@gmail.com",
            "password": "12345678",
            "phone": "+8801815553038",
            "first_name": "osman",
            "last_name": "goni",
        }
        response = self.client.post(reverse("user-registration"), data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
