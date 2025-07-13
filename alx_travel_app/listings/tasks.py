#!/usr/bin/env python3
"""
Celery task for sending booking confirmation emails.
"""
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(email: str, booking_id: int) -> None:
    """
    Sends an email confirming a booking.
    """
    send_mail(
        subject="Booking Confirmation",
        message=f"Your booking with ID {booking_id} was successful!",
        from_email="your_email@example.com",
        recipient_list=[email],
        fail_silently=False,
    )
