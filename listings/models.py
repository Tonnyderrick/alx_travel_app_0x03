
# Create your models here.
from django.db import models

class Payment(models.Model):
    booking_reference = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.status}"
