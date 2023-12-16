from django.urls import reverse

from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)

from core.models import User


class AdminProductAPITestCase(APITestCase):
    """Written BaseAPITestCase for not repeating the same code in the test"""

    def setUp(self):
        self.client = APIClient()

        user = User.objects.create_superuser("+8801815553036", "12345678")

        self.user_login = self.client.post(
            reverse("token_obtain_pair"),
            data={"phone": "+8801815553036", "password": "12345678"},
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"],
            HTTP_X_DOMAIN="bill-corp",
        )

    def test_admin_product_create(self):
        payload = {
            "title": "Test Product",
            "price": 3000,
            "discount": 10.0,
            "quantity": 200,
            "status": "PUBLISHED",
        }
        response = self.client.post(reverse("admin-products-list"), data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_products_list_(self):
        payload = {
            "title": "Test Product",
            "price": 3000,
            "discount": 10.0,
            "quantity": 200,
            "status": "PUBLISHED",
        }
        self.client.post(reverse("admin-products-list"), data=payload)
        response = self.client.get(reverse("admin-products-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
