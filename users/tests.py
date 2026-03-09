from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import ProductManagementEnrollment

class ProductManagementEnrollmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:enroll_product_management')

    def test_enroll_success(self):
        data = {
            "full_name": "Test User",
            "email_address": "test@example.com",
            "phone_number": "1234567890"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductManagementEnrollment.objects.count(), 1)
        self.assertEqual(ProductManagementEnrollment.objects.get().full_name, 'Test User')

    def test_enroll_missing_fields(self):
        data = {
            "full_name": "Test User"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
