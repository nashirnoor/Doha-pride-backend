from django.db import models
from django.utils.translation import gettext_lazy as _
from ToursAndActivities.models import ToursAndActivities
from django.core.mail import send_mail
from django.conf import settings
from app.models import TransferMeetAssist
from django.contrib.auth import get_user_model
import random


class TourBooking(models.Model):
    STATUS_CHOICES = (
        ('done', 'Done'),
        ('pending', 'Pending'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    )
    tour_activity = models.ForeignKey(ToursAndActivities, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.status == 'rejected' and self.rejection_reason:
            self.send_rejection_email()
        super().save(*args, **kwargs)

    def send_rejection_email(self):
        subject = 'Booking Rejected'
        message = f'Dear {self.name},\n\nWe regret to inform you that your booking has been rejected.\n\nReason: {self.rejection_reason}\n\nThank you for your understanding.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.email]
        send_mail(subject, message, from_email, recipient_list)

class TransferBooking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
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