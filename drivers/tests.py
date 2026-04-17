from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Driver

class DriverTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_driver(self):
        response = self.client.post('/api/drivers/', {
            'name': 'John Doe',
            'license_number': 'LIC123',
            'phone_number': '0771234567'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Driver.objects.count(), 1)

    def test_get_drivers(self):
        Driver.objects.create(
            name='John Doe',
            license_number='LIC123',
            phone_number='0771234567'
        )
        response = self.client.get('/api/drivers/')
        self.assertEqual(response.status_code, 200)

    def test_update_driver(self):
        driver = Driver.objects.create(
            name='John Doe',
            license_number='LIC123',
            phone_number='0771234567'
        )
        response = self.client.put(f'/api/drivers/{driver.driver_id}/', {
            'name': 'Jane Doe',
            'license_number': 'LIC123',
            'phone_number': '0779999999'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        driver.refresh_from_db()
        self.assertEqual(driver.name, 'Jane Doe')

    def test_delete_driver(self):
        driver = Driver.objects.create(
            name='John Doe',
            license_number='LIC123',
            phone_number='0771234567'
        )
        response = self.client.delete(f'/api/drivers/{driver.driver_id}/')
        self.assertEqual(response.status_code, 204)