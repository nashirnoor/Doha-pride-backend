from django.db import models
from django.utils.translation import gettext_lazy as _
from ToursAndActivities.models import ToursAndActivities
from django.core.mail import send_mail
from django.conf import settings
from app.models import TransferMeetAssist
from django.contrib.auth import get_user_model
import random
from threading import local

_thread_locals = local()


class TourBooking(models.Model):
    STATUS_CHOICES = (
        ('done', 'Done'),
        ('pending', 'Pending'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    )
    tour_activity = models.ForeignKey(ToursAndActivities, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    number = models.CharField(max_length=20,null=True,blank=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    driver = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='tour_bookings')
    rejection_reason = models.TextField(blank=True, null=True)
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    vehicle = models.CharField(max_length=100, blank=True, null=True)
    flight = models.CharField(max_length=100, blank=True, null=True)
    room_no = models.CharField(max_length=50, blank=True, null=True)
    amount = models.CharField(max_length=20,blank=True,null=True)
    voucher_no = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    unique_code = models.CharField(max_length=5, unique=True, editable=False, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.unique_code}"

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = self.generate_unique_code()
        if self.status == 'rejected' and self.rejection_reason:
            self.send_rejection_email()
        super().save(*args, **kwargs)

    
    def generate_unique_code(self):
        """Generates a unique 5-digit random number."""
        code = random.randint(1000, 99999)
        while TransferBooking.objects.filter(unique_code=code).exists():
            code = random.randint(1000, 99999)
        return str(code)

    def send_rejection_email(self):
        subject = 'Booking Rejected'
        message = f'Dear {self.name},\n\nWe regret to inform you that your booking has been rejected.\n\nReason: {self.rejection_reason}\n\nThank you for your understanding.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]
        send_mail(subject, message, from_email, recipient_list)

class TransferBooking(models.Model):
    STATUS_CHOICES = (
        ('done', 'Done'),
        ('pending', 'Pending'),
        ('posted', 'Posted'),
        ('ongoing','OnGoing'),
        ('cancelled', 'Cancelled'),
    )
    transfer_name = models.ForeignKey(TransferMeetAssist, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    number = models.CharField(max_length=20,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    from_location = models.CharField(max_length=255, blank=True, null=True)
    to_location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    driver = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='transfer_bookings')
    # New fields
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    vehicle = models.CharField(max_length=100, blank=True, null=True)
    flight = models.CharField(max_length=100, blank=True, null=True)
    room_no = models.CharField(max_length=50, blank=True, null=True)
    amount = models.CharField(max_length=20,blank=True,null=True)
    voucher_no = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    unique_code = models.CharField(max_length=5, unique=True, editable=False, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.unique_code}"

    def save(self, *args, **kwargs):
        print("Save method called")
        
        # Get current_user from instance attribute or kwargs
        current_user = kwargs.pop('_current_user', None) or getattr(self, '_current_user', None)
        print(f"Current user in save: {current_user}")
        
        # Store current_user before calling super().save()
        self._current_user = current_user
        
        if not self.unique_code:
            self.unique_code = self.generate_unique_code()
        if self.status == 'rejected' and self.rejection_reason:
            self.send_rejection_email()
        
        super().save(*args, **kwargs)

    
    def generate_unique_code(self):
        """Generates a unique 5-digit random number."""
        code = random.randint(1000, 99999)
        while TransferBooking.objects.filter(unique_code=code).exists():
            code = random.randint(1000, 99999)
        return str(code)
    

    def send_rejection_email(self):
        subject = 'Booking Rejected'
        message = f'Dear {self.name},\n\nWe regret to inform you that your booking has been rejected.\n\nReason: {self.rejection_reason}\n\nThank you for your understanding.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]
        send_mail(subject, message, from_email, recipient_list)


class TransferBookingAudit(models.Model):
    ACTION_CHOICES = (
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
    )
    
    transfer_booking = models.ForeignKey('TransferBooking', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']




class HotelCategory(models.Model):
    hotel_name = models.CharField(max_length=255)

    def __str__(self):
        return self.hotel_name
    

class HotelSubcategory(models.Model):
    category = models.ForeignKey(HotelCategory, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.category.hotel_name})"
    
