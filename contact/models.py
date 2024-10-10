from django.db import models

class Contact(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.email  # Can be any field to represent the model in admin
