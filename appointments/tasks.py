from celery import shared_task

@shared_task
def send_appointment_confirmation(appointment_id):
    # Logic to send confirmation email
    pass 