from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Job
from trucks.models import Truck
from drivers.models import Driver

class JobTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create truck and driver for tests
        self.truck = Truck.objects.create(
            registration_number='ZW 1234',
            capacity=5000,
            status='AVAILABLE'
        )
        self.driver = Driver.objects.create(
            name='John Doe',
            license_number='LIC123',
            phone_number='0771234567'
        )

    def test_create_job(self):
        response = self.client.post('/api/jobs/', {
            'pickup_location': 'Harare CBD',
            'delivery_location': 'Bulawayo',
            'cargo_description': 'Building materials',
            'status': 'PENDING',
            'assigned_truck': self.truck.truck_id,
            'assigned_driver': self.driver.driver_id
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_cannot_assign_truck_under_maintenance(self):
        self.truck.status = 'UNDER_MAINTENANCE'
        self.truck.save()
        response = self.client.post('/api/jobs/', {
            'pickup_location': 'Harare CBD',
            'delivery_location': 'Mutare',
            'cargo_description': 'Electronics',
            'status': 'PENDING',
            'assigned_truck': self.truck.truck_id,
            'assigned_driver': self.driver.driver_id
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_cannot_assign_driver_with_active_job(self):
        # Create first active job
        Job.objects.create(
            pickup_location='Harare',
            delivery_location='Bulawayo',
            cargo_description='Furniture',
            status='IN_TRANSIT',
            assigned_truck=self.truck,
            assigned_driver=self.driver
        )
        # Try to create second job with same driver
        response = self.client.post('/api/jobs/', {
            'pickup_location': 'Gweru',
            'delivery_location': 'Masvingo',
            'cargo_description': 'Cement',
            'status': 'PENDING',
            'assigned_truck': self.truck.truck_id,
            'assigned_driver': self.driver.driver_id
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_truck_status_updates_when_job_in_transit(self):
        job = Job.objects.create(
            pickup_location='Harare',
            delivery_location='Bulawayo',
            cargo_description='Furniture',
            status='PENDING',
            assigned_truck=self.truck,
            assigned_driver=self.driver
        )
        self.client.put(f'/api/jobs/{job.job_id}/', {
            'pickup_location': 'Harare',
            'delivery_location': 'Bulawayo',
            'cargo_description': 'Furniture',
            'status': 'IN_TRANSIT',
            'assigned_truck': self.truck.truck_id,
            'assigned_driver': self.driver.driver_id
        }, format='json')
        self.truck.refresh_from_db()
        self.assertEqual(self.truck.status, 'IN_TRANSIT')

    def test_truck_becomes_available_when_job_delivered(self):
        job = Job.objects.create(
            pickup_location='Harare',
            delivery_location='Bulawayo',
            cargo_description='Furniture',
            status='IN_TRANSIT',
            assigned_truck=self.truck,
            assigned_driver=self.driver
        )
        self.client.put(f'/api/jobs/{job.job_id}/', {
            'pickup_location': 'Harare',
            'delivery_location': 'Bulawayo',
            'cargo_description': 'Furniture',
            'status': 'DELIVERED',
            'assigned_truck': self.truck.truck_id,
            'assigned_driver': self.driver.driver_id
        }, format='json')
        self.truck.refresh_from_db()
        self.assertEqual(self.truck.status, 'AVAILABLE')