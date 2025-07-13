from django.shortcuts import render

# Create your views here.
from .tasks import send_booking_confirmation_email

class BookingViewSet(viewsets.ModelViewSet):
    # ...
    def perform_create(self, serializer):
        booking = serializer.save()
        send_booking_confirmation_email.delay(
            booking.customer.email,
            booking.id
        )
