from django.db import models

class Contact(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.email  # Can be any field to represent the model in admin


class ContactMessage(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('noted', 'Noted'),
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    def __str__(self):
        return f"Message from {self.name} - {self.email}"