from rest_framework import serializers
from .models import Appointment
from doctors.serializers import DoctorSerializer
from patients.serializers import PatientSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    patient_details = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'patient', 'patient_details', 'doctor', 'doctor_details',
                 'appointment_date', 'start_time', 'end_time', 'status',
                 'reason', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, attrs):
        # Check if the appointment time is within doctor's availability
        doctor = attrs['doctor']
        appointment_date = attrs['appointment_date']
        start_time = attrs['start_time']
        end_time = attrs['end_time']

        # Check if doctor is available at the requested time
        if not doctor.availabilities.filter(
            day=appointment_date.strftime('%A').lower(),
            start_time__lte=start_time,
            end_time__gte=end_time,
            is_available=True
        ).exists():
            raise serializers.ValidationError("Doctor is not available at this time")

        # Check for scheduling conflicts
        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=['scheduled', 'confirmed']
        ).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("This time slot is already booked")

        return attrs

class AppointmentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('status', 'notes')

    def validate_status(self, value):
        if self.instance and self.instance.status == 'completed' and value != 'completed':
            raise serializers.ValidationError("Cannot change status of a completed appointment")
        return value 