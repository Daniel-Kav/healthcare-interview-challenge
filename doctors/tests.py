from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Doctor, Specialization, DoctorAvailability
from users.models import User

User = get_user_model()

class SpecializationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            user_type='admin'
        )
        self.client.force_authenticate(user=self.user)
        self.specialization_url = reverse('specialization-list')
        self.valid_payload = {
            'name': 'Cardiology',
            'description': 'Heart specialist'
        }

    def test_create_specialization(self):
        response = self.client.post(self.specialization_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Specialization.objects.count(), 1)
        self.assertEqual(Specialization.objects.get().name, 'Cardiology')

    def test_list_specializations(self):
        Specialization.objects.create(name='Cardiology', description='Heart specialist')
        Specialization.objects.create(name='Neurology', description='Brain specialist')
        response = self.client.get(self.specialization_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class DoctorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='doctor',
            email='doctor@example.com',
            password='doctorpass123',
            user_type='doctor'
        )
        self.specialization = Specialization.objects.create(
            name='Cardiology',
            description='Heart specialist'
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DOC123',
            years_of_experience=5,
            consultation_fee=100.00
        )
        self.client.force_authenticate(user=self.user)
        self.doctor_url = reverse('doctor-list')
        self.doctor_detail_url = reverse('doctor-detail', kwargs={'pk': self.doctor.pk})

    def test_get_doctor_list(self):
        response = self.client.get(self.doctor_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_doctor_detail(self):
        response = self.client.get(self.doctor_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['license_number'], 'DOC123')

    def test_update_doctor(self):
        update_data = {
            'years_of_experience': 6,
            'consultation_fee': 120.00
        }
        response = self.client.patch(self.doctor_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.years_of_experience, 6)
        self.assertEqual(float(self.doctor.consultation_fee), 120.00)

class DoctorAvailabilityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='doctor',
            email='doctor@example.com',
            password='doctorpass123',
            user_type='doctor'
        )
        self.specialization = Specialization.objects.create(
            name='Cardiology',
            description='Heart specialist'
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DOC123',
            years_of_experience=5,
            consultation_fee=100.00
        )
        self.client.force_authenticate(user=self.user)
        self.availability_url = reverse('doctor-availability', kwargs={'doctor_id': self.doctor.pk})
        self.valid_payload = {
            'day': 'monday',
            'start_time': '09:00:00',
            'end_time': '17:00:00',
            'is_available': True
        }

    def test_create_availability(self):
        response = self.client.post(self.availability_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DoctorAvailability.objects.count(), 1)

    def test_bulk_create_availability(self):
        bulk_url = reverse('doctor-availability-bulk', kwargs={'doctor_id': self.doctor.pk})
        bulk_data = {
            'availabilities': [
                {
                    'day': 'monday',
                    'start_time': '09:00:00',
                    'end_time': '17:00:00',
                    'is_available': True
                },
                {
                    'day': 'tuesday',
                    'start_time': '09:00:00',
                    'end_time': '17:00:00',
                    'is_available': True
                }
            ]
        }
        response = self.client.post(bulk_url, bulk_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DoctorAvailability.objects.count(), 2)
