from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_appointment_confirmation

# Create your models here.

@receiver(post_save, sender=Appointment)
def appointment_created(sender, instance, created, **kwargs):
    if created:
        # Send confirmation email asynchronously
        send_appointment_confirmation.delay(instance.id)
