from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import TransferBooking,TransferBookingAudit
@receiver(pre_save, sender=TransferBooking)
def track_transfer_booking_changes(sender, instance, **kwargs):
    if instance.pk:  # If this is an update
        old_instance = TransferBooking.objects.get(pk=instance.pk)
        for field in instance._meta.fields:
            old_value = getattr(old_instance, field.name)
            new_value = getattr(instance, field.name)
            
            if old_value != new_value:
                # Get the current user from thread local storage
                user = getattr(instance, '_current_user', None)
                
                TransferBookingAudit.objects.create(
                    transfer_booking=instance,
                    user=user,
                    action='update',
                    field_name=field.name,
                    old_value=str(old_value),
                    new_value=str(new_value)
                )

@receiver(post_save, sender=TransferBooking)
def track_transfer_booking_creation(sender, instance, created, **kwargs):
    if created:
        user = getattr(instance, '_current_user', None)
        TransferBookingAudit.objects.create(
            transfer_booking=instance,
            user=user,
            action='create',
            field_name='record',
            new_value='Created new transfer booking'
        )