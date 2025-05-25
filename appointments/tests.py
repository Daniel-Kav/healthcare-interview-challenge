from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from users.models import User
from doctors.models import Doctor, Specialization, DoctorAvailability
from patients.models import Patient

User = get_user_model()

class AppointmentTests(APITestCase):
    def setUp(self):
        # Create a doctor
        self.doctor_user = User.objects.create_user(
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
            user=self.doctor_user,
            specialization=self.specialization,
            license_number='DOC123',
            years_of_experience=5,
            consultation_fee=100.00
        )
        
        # Create doctor availability
        self.availability = DoctorAvailability.objects.create(
            doctor=self.doctor,
            day='monday',
            start_time='09:00:00',
            end_time='17:00:00',
            is_available=True
        )
        
        # Create a patient
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
        
        # Create an appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().date() + timedelta(days=1),
            start_time='10:00:00',
            end_time='11:00:00',
            status='scheduled',
            reason='Regular checkup'
        )
        
        self.client.force_authenticate(user=self.patient_user)
        self.appointment_url = reverse('appointment-list')
        self.appointment_detail_url = reverse('appointment-detail', kwargs={'pk': self.appointment.pk})

    def test_create_appointment(self):
        new_appointment_data = {
            'doctor': self.doctor.id,
            'appointment_date': (timezone.now().date() + timedelta(days=2)).isoformat(),
            'start_time': '14:00:00',
            'end_time': '15:00:00',
            'reason': 'Follow-up consultation'
        }
        response = self.client.post(self.appointment_url, new_appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)

    def test_get_appointment_list(self):
        response = self.client.get(self.appointment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_appointment_detail(self):
        response = self.client.get(self.appointment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reason'], 'Regular checkup')

    def test_update_appointment_status(self):
        self.client.force_authenticate(user=self.doctor_user)
        status_url = reverse('appointment-status-update', kwargs={'pk': self.appointment.pk})
        update_data = {
            'status': 'confirmed',
            'notes': 'Appointment confirmed'
        }
        response = self.client.patch(status_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'confirmed')
        self.assertEqual(self.appointment.notes, 'Appointment confirmed')

    def test_cannot_schedule_outside_availability(self):
        new_appointment_data = {
            'doctor': self.doctor.id,
            'appointment_date': (timezone.now().date() + timedelta(days=2)).isoformat(),
            'start_time': '08:00:00',  # Before doctor's availability
            'end_time': '09:00:00',
            'reason': 'Early morning appointment'
        }
        response = self.client.post(self.appointment_url, new_appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_schedule_conflicting_appointment(self):
        # Create another appointment at the same time
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=self.appointment.appointment_date,
            start_time='10:00:00',
            end_time='11:00:00',
            status='scheduled',
            reason='Another appointment'
        )
        
        # Try to create a conflicting appointment
        new_appointment_data = {
            'doctor': self.doctor.id,
            'appointment_date': self.appointment.appointment_date.isoformat(),
            'start_time': '10:30:00',
            'end_time': '11:30:00',
            'reason': 'Conflicting appointment'
        }
        response = self.client.post(self.appointment_url, new_appointment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
