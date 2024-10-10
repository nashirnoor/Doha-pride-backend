from django.db import models
from django.utils.translation import gettext_lazy as _
from ToursAndActivities.models import ToursAndActivities
from django.core.mail import send_mail
from django.conf import settings
from app.models import TransferMeetAssist

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
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
    transfer_name = models.ForeignKey(TransferMeetAssist, on_delete=models.CASCADE,null=True,blank=True)
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





