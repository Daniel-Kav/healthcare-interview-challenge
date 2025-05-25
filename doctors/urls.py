from django.urls import path
from .views import (
    SpecializationListView,
    SpecializationDetailView,
    DoctorListView,
    DoctorDetailView,
    DoctorAvailabilityView,
    DoctorAvailabilityBulkCreateView,
)

urlpatterns = [
    # Specialization endpoints
    path('specializations/', SpecializationListView.as_view(), name='specialization-list'),
    path('specializations/<int:pk>/', SpecializationDetailView.as_view(), name='specialization-detail'),
    
    # Doctor endpoints
    path('', DoctorListView.as_view(), name='doctor-list'),
    path('<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    
    # Doctor availability endpoints
    path('<int:doctor_id>/availability/', DoctorAvailabilityView.as_view(), name='doctor-availability'),
    path('<int:doctor_id>/availability/bulk/', DoctorAvailabilityBulkCreateView.as_view(), name='doctor-availability-bulk'),
] 