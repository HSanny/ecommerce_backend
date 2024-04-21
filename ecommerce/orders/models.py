from django.db import models
from django.conf import settings

class Order(models.Model):

    status_choices = [
        ('paid', 'Paid'),
        ('preparing', 'Preparing for Shipment'),
        ('shipped', 'Shipped'),
        ('arrived', 'Arrived'),
        ('completed', 'Order Complete'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    address = models.TextField()
    payment_details = models.JSONField() # Assuming payment details are stored in a JSON format
    status = models.CharField(max_length=20, choices=status_choices, default='paid')

    # TODO: ... additional fields for order such as timestamp, total amount, etc.

    def mark_as_completed(self):
        self.status = 'completed'
        self.save()