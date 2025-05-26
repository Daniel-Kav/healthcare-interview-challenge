from django.urls import path
from .views import (
    PatientListView,
    PatientDetailView,
    MedicalRecordListView,
    MedicalRecordDetailView,
)

urlpatterns = [
    # Patient endpoints
    path('', PatientListView.as_view(), name='patient-list'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    
    # Medical records endpoints
    path('<int:patient_id>/records/', MedicalRecordListView.as_view(), name='medical-record-list'),
    path('<int:patient_id>/records/<int:pk>/', MedicalRecordDetailView.as_view(), name='medical-record-detail'),
] 