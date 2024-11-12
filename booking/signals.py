from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import TransferBooking,TransferBookingAudit,TourBooking,TourBookingAudit
from .middleware import _thread_locals
from django.contrib.auth.models import AnonymousUser

@receiver(post_save, sender=TransferBooking)
def track_transfer_booking_creation(sender, instance, created, **kwargs):
    print("Post-save signal triggered")
    if not created:  # Exit early if this is not a creation
        return

    current_user = getattr(instance, '_current_user', None)
    print(f"User in post_save signal: {current_user}")

    # Initialize existing_audit as None
    existing_audit = None

    # Only proceed with audit if we have a valid user
    if current_user and not isinstance(current_user, AnonymousUser):
        # Check for existing audit
        existing_audit = TransferBookingAudit.objects.filter(
            transfer_booking=instance,
            action='create',
            field_name='booking'
        ).first()

        if not existing_audit:
            try:
                TransferBookingAudit.objects.create(
                    transfer_booking=instance,
                    user=current_user,
                    action='create',
                    field_name='booking',
                    old_value=None,
                    new_value=f"Created booking for {instance.name}"
                )
            except Exception as e:
                print(f"Error creating audit entry: {str(e)}")

@receiver(pre_save, sender=TransferBooking)
def track_transfer_booking_changes(sender, instance, **kwargs):
    if instance.pk:  # Only for existing instances
        current_user = getattr(instance, '_current_user', None)
        print(f"User in pre_save signal: {current_user}")

        # Skip audit creation if user is anonymous or None
        if current_user and not isinstance(current_user, AnonymousUser):
            try:
                old_instance = TransferBooking.objects.get(pk=instance.pk)
                fields_to_track = [
                    'name', 'email', 'number', 'date', 'time', 'from_location', 'to_location',
                    'status', 'rejection_reason', 'driver', 'hotel_name',
                    'vehicle', 'flight', 'room_no', 'amount', 'voucher_no', 'note'
                ]

                for field in fields_to_track:
                    old_value = getattr(old_instance, field)
                    new_value = getattr(instance, field)
                    
                    # Add debug print statements
                    print(f"Checking field {field}: old={old_value}, new={new_value}")
                    
                    if old_value != new_value:
                        print(f"Change detected in {field}")
                        TransferBookingAudit.objects.create(
                            transfer_booking=instance,
                            user=current_user,
                            action='update',
                            field_name=field,
                            old_value=str(old_value) if old_value is not None else '',
                            new_value=str(new_value) if new_value is not None else ''
                        )
            except TransferBooking.DoesNotExist:
                print("TransferBooking instance not found")
                pass
        else:
            print(f"Skipping audit: current_user={current_user}")

@receiver(post_save, sender=TourBooking)
def track_tour_booking_creation(sender, instance, created, **kwargs):
    print("Post-save signal triggered")
    if not created:  # Exit early if this is not a creation
        return

    current_user = getattr(instance, '_current_user', None)
    print(f"User in post_save signal: {current_user}")

    # Initialize existing_audit as None
    existing_audit = None

    # Only proceed with audit if we have a valid user
    if current_user and not isinstance(current_user, AnonymousUser):
        # Check for existing audit
        existing_audit = TourBookingAudit.objects.filter(
            tour_booking=instance,
            action='create',
            field_name='booking'
        ).first()

        if not existing_audit:
            try:
                TourBookingAudit.objects.create(
                    tour_booking=instance,
                    user=current_user,
                    action='create',
                    field_name='booking',
                    old_value=None,
                    new_value=f"Created booking for {instance.name}"
                )
            except Exception as e:
                print(f"Error creating audit entry: {str(e)}")

@receiver(pre_save, sender=TourBooking)
def track_tour_booking_changes(sender, instance, **kwargs):
    if not instance.pk:  # Skip if this is a new instance
        return

    current_user = getattr(instance, '_current_user', None)
    print(f"User in pre_save signal: {current_user}")

    # Only proceed with audit if we have a valid user
    if current_user and not isinstance(current_user, AnonymousUser):
        try:
            old_instance = TourBooking.objects.get(pk=instance.pk)
            fields_to_track = [
                'name', 'email', 'number', 'date', 'time', 'payment_type','currency',
                'status', 'rejection_reason', 'driver', 'hotel_name',
                'vehicle', 'flight', 'room_no', 'amount', 'voucher_no', 'note'
            ]

            for field in fields_to_track:
                old_value = getattr(old_instance, field)
                new_value = getattr(instance, field)
                
                if old_value != new_value:
                    try:
                        TourBookingAudit.objects.create(
                            tour_booking=instance,
                            user=current_user,
                            action='update',
                            field_name=field,
                            old_value=str(old_value),
                            new_value=str(new_value)
                        )
                    except Exception as e:
                        print(f"Error creating audit entry for field {field}: {str(e)}")
        except TourBooking.DoesNotExist:
            print("Previous instance not found")
        except Exception as e:
            print(f"Error in tracking changes: {str(e)}")