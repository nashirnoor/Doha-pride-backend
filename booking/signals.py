from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import TransferBooking,TransferBookingAudit,TourBooking,TourBookingAudit

@receiver(pre_save, sender=TransferBooking)
def track_transfer_booking_changes(sender, instance, **kwargs):
    print("Signals triggered for transfer booking changes")
    if instance.pk:  # If this is an update
        old_instance = TransferBooking.objects.get(pk=instance.pk)
        current_user = getattr(instance, '_current_user', None)
        print(f"Current user in signal: {current_user}")  # Debug print

        for field in instance._meta.fields:
            old_value = getattr(old_instance, field.name)
            new_value = getattr(instance, field.name)
            
            if old_value != new_value:
                # Get the current user from thread local storage
                user = getattr(instance, '_current_user', None)
                print(f"Creating audit for field {field.name}")  # Debug print
                print(f"User for audit: {current_user}") 
                
                TransferBookingAudit.objects.create(
                    transfer_booking=instance,
                    user=current_user,
                    action='update',
                    field_name=field.name,
                    old_value=str(old_value),
                    new_value=str(new_value)
                )

@receiver(post_save, sender=TransferBooking)
def track_transfer_booking_creation(sender, instance, created, **kwargs):
    print("Post-save signal triggered")
    if created:
        current_user = getattr(instance, '_current_user', None)
        print(f"User in post_save signal: {current_user}")
        
        if current_user:
            TransferBookingAudit.objects.create(
                transfer_booking=instance,
                user=current_user,
                action='create',
                field_name='record',
                new_value='Created new transfer booking'
            )
        else:
            print("Warning: No user found for audit creation")



@receiver(pre_save, sender=TourBooking)
def track_tour_booking_changes(sender, instance, **kwargs):
    print("Signals triggered for Tour booking changes")
    if instance.pk:  # If this is an update
        old_instance = TourBooking.objects.get(pk=instance.pk)
        current_user = getattr(instance, '_current_user', None)
        print(f"Current user in signal: {current_user}")  # Debug print

        for field in instance._meta.fields:
            old_value = getattr(old_instance, field.name)
            new_value = getattr(instance, field.name)
            
            if old_value != new_value:
                user = getattr(instance, '_current_user', None)
                print(f"Creating audit for field {field.name}")  # Debug print
                print(f"User for audit: {current_user}") 
                
                TourBookingAudit.objects.create(
                    transfer_booking=instance,
                    user=current_user,
                    action='update',
                    field_name=field.name,
                    old_value=str(old_value),
                    new_value=str(new_value)
                )

@receiver(post_save, sender=TourBooking)
def track_transfer_booking_creation(sender, instance, created, **kwargs):
    print("Post-save signal triggered")
    if created:
        current_user = getattr(instance, '_current_user', None)
        print(f"User in post_save signal: {current_user}")
        
        if current_user:
            TourBooking.objects.create(
                tour_booking=instance,
                user=current_user,
                action='create',
                field_name='record',
                new_value='Created new transfer booking'
            )
        else:
            print("Warning: No user found for audit creation")