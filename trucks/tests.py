from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Truck

class TruckTests(TestCase):

    def setUp(self):
       
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_truck(self):
        response = self.client.post('/api/trucks/', {
            'registration_number': 'ZW 1234',
            'capacity': 5000,
            'status': 'AVAILABLE'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Truck.objects.count(), 1)

    def test_get_trucks(self):
        Truck.objects.create(
            registration_number='ZW 1234',
            capacity=5000,
            status='AVAILABLE'
        )
        response = self.client.get('/api/trucks/')
        self.assertEqual(response.status_code, 200)

    def test_update_truck(self):
        truck = Truck.objects.create(
            registration_number='ZW 1234',
            capacity=5000,
            status='AVAILABLE'
        )
        response = self.client.put(f'/api/trucks/{truck.truck_id}/', {
            'registration_number': 'ZW 1234',
            'capacity': 5000,
            'status': 'UNDER_MAINTENANCE'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        truck.refresh_from_db()
        self.assertEqual(truck.status, 'UNDER_MAINTENANCE')

    def test_delete_truck_in_transit(self):
        truck = Truck.objects.create(
            registration_number='ZW 5678',
            capacity=3000,
            status='IN_TRANSIT'
        )
        response = self.client.delete(f'/api/trucks/{truck.truck_id}/')
        self.assertEqual(response.status_code, 400)

    def test_delete_available_truck(self):
        truck = Truck.objects.create(
            registration_number='ZW 9999',
            capacity=3000,
            status='AVAILABLE'
        )
        response = self.client.delete(f'/api/trucks/{truck.truck_id}/')
        self.assertEqual(response.status_code, 204)