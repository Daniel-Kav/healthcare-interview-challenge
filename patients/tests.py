from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Patient, MedicalRecord
from users.models import User

User = get_user_model()

class PatientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='patient',
            email='patient@example.com',
            password='patientpass123',
            user_type='patient'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            blood_type='A+',
            allergies='None',
            chronic_conditions='None',
            emergency_contact_name='Emergency Contact',
            emergency_contact_phone='1234567890',
            insurance_provider='Test Insurance',
            insurance_policy_number='POL123'
        )
        self.client.force_authenticate(user=self.user)
        self.patient_url = reverse('patient-list')
        self.patient_detail_url = reverse('patient-detail', kwargs={'pk': self.patient.pk})

    def test_get_patient_list(self):
        response = self.client.get(self.patient_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_patient_detail(self):
        response = self.client.get(self.patient_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['blood_type'], 'A+')
        self.assertEqual(response.data['insurance_policy_number'], 'POL123')

    def test_update_patient(self):
        update_data = {
            'allergies': 'Penicillin',
            'emergency_contact_phone': '9876543210'
        }
        response = self.client.patch(self.patient_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.allergies, 'Penicillin')
        self.assertEqual(self.patient.emergency_contact_phone, '9876543210')

class MedicalRecordTests(APITestCase):
    def setUp(self):
        # Create a doctor user
        self.doctor_user = User.objects.create_user(
            username='doctor',
            email='doctor@example.com',
            password='doctorpass123',
            user_type='doctor'
        )
        
        # Create a patient user and profile
        self.patient_user = User.objects.create_user(
            username='patient',
            email='patient@example.com',
            password='patientpass123',
            user_type='patient'
        )
        self.patient = Patient.objects.create(
            user=self.patient_user,
            blood_type='A+'
        )
        
        # Create a medical record
        self.medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            diagnosis='Common cold',
            prescription='Rest and fluids',
            notes='Patient should rest for 3 days',
            date='2024-03-20'
        )
        
        self.client.force_authenticate(user=self.doctor_user)
        self.records_url = reverse('medical-record-list', kwargs={'patient_id': self.patient.pk})
        self.record_detail_url = reverse('medical-record-detail', 
                                       kwargs={'patient_id': self.patient.pk, 'pk': self.medical_record.pk})

    def test_create_medical_record(self):
        new_record_data = {
            'diagnosis': 'Flu',
            'prescription': 'Tamiflu',
            'notes': 'Take medication as prescribed',
            'date': '2024-03-21'
        }
        response = self.client.post(self.records_url, new_record_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalRecord.objects.count(), 2)

    def test_get_medical_records(self):
        response = self.client.get(self.records_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_medical_record(self):
        update_data = {
            'diagnosis': 'Severe cold',
            'notes': 'Patient should rest for 5 days'
        }
        response = self.client.patch(self.record_detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medical_record.refresh_from_db()
        self.assertEqual(self.medical_record.diagnosis, 'Severe cold')
        self.assertEqual(self.medical_record.notes, 'Patient should rest for 5 days')

    def test_patient_cannot_create_medical_record(self):
        self.client.force_authenticate(user=self.patient_user)
        new_record_data = {
            'diagnosis': 'Self-diagnosis',
            'prescription': 'None',
            'notes': 'I think I have a cold',
            'date': '2024-03-21'
        }
        response = self.client.post(self.records_url, new_record_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
