from django.db import models

class Contact(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.email  # Can be any field to represent the model in admin


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
