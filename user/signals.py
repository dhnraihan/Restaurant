from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Order, Invoice
import random
import string

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a Profile for every new User"""
    if created:
        Profile.objects.create(user=instance)


def create_or_update_invoice(sender, instance, created, **kwargs):
    # Check if the Order instance was just created
    if created:
        # Check if an invoice doesn't already exist for this order (optional but safe)
        if not hasattr(instance, 'invoice'):
            # Create the invoice only for new orders
            Invoice.objects.create(
                order=instance,
                # Add other necessary fields for the invoice, like amount
                amount=instance.total_amount
                # You might have logic here to generate an invoice number, etc.
            )