# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('customer', 'Customer'),
        ('staff','Staff'),
        ('travel_agency','Travel Agency')
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_type']

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Banner(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='banners/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title or f"Banner {self.id}"


class DriverFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_feedbacks',null=True,blank=True)
    image = models.ImageField(upload_to='driver_feedback/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Driver Feedback {self.id} - {self.user.username if self.user else 'No User'}"