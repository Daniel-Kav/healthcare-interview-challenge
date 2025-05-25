from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Doctor, Specialization, DoctorAvailability
from .serializers import (
    DoctorSerializer,
    SpecializationSerializer,
    DoctorAvailabilitySerializer,
    DoctorAvailabilityBulkCreateSerializer
)

# Create your views here.

class SpecializationListView(generics.ListCreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [permissions.IsAuthenticated]

class SpecializationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [permissions.IsAuthenticated]

class DoctorListView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['specialization', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'license_number']
    ordering_fields = ['years_of_experience', 'consultation_fee']

class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

class DoctorAvailabilityView(generics.ListCreateAPIView):
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return DoctorAvailability.objects.filter(doctor_id=doctor_id)

    def perform_create(self, serializer):
        doctor_id = self.kwargs.get('doctor_id')
        doctor = get_object_or_404(Doctor, id=doctor_id)
        serializer.save(doctor=doctor)

class DoctorAvailabilityBulkCreateView(generics.CreateAPIView):
    serializer_class = DoctorAvailabilityBulkCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_doctor(self):
        doctor_id = self.kwargs.get('doctor_id')
        return get_object_or_404(Doctor, id=doctor_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(doctor=self.get_doctor())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
