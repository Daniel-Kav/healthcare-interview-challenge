from rest_framework import serializers
from .models import Patient, MedicalRecord
from users.serializers import UserSerializer

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    medical_records = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ('id', 'user', 'blood_type', 'allergies', 'chronic_conditions',
                 'emergency_contact_name', 'emergency_contact_phone',
                 'insurance_provider', 'insurance_policy_number',
                 'medical_records', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_medical_records(self, obj):
        records = obj.medical_records.all()[:5]  # Get only the 5 most recent records
        return MedicalRecordSerializer(records, many=True).data

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = ('id', 'patient', 'patient_name', 'diagnosis', 'prescription',
                 'notes', 'date', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()

    def validate(self, attrs):
        # Ensure the user has permission to create/edit medical records
        request = self.context.get('request')
        if request and not request.user.is_staff and not request.user.user_type == 'doctor':
            raise serializers.ValidationError("Only doctors and staff can create/edit medical records")
        return attrs 