from django.db import models
from django.utils import timezone


class TourImage(models.Model):
    image = models.ImageField(upload_to='tours/')
    alt_text = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.alt_text if self.alt_text else "Tour Image"


class ToursAndActivities(models.Model):
    CATEGORY_CHOICES = [
        ('Food & Drink', 'Food & Drink'),
        ('Sport', 'Sport'),
        ('City Tour', 'City Tour'),
        ('Shopping', 'Shopping'),
        ('Adventure', 'Adventure'),
        ('Art', 'Art'),
        ('Culture', 'Culture'),
        ('Art Culture', 'Art Culture'),
        ('Adventure Nature', 'Adventure Nature'),
    ]
    
    DURATION_CHOICES = [
        ('1 hr', '1 hr'),
        ('2 hr', '2 hr'),
        ('3 hr', '3 hr'),
        ('4 hr', '4 hr'),
        ('5 hr', '5 hr'),
        ('6 hr', '6 hr'),
        ('half day', 'Half Day'),
        ('full day', 'Full Day'),
        ('2 day', '2 Day'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=3000)
    image = models.ImageField(upload_to='tour_images/', null=True, blank=True)
    media_gallery = models.ManyToManyField('TourImage', related_name='tours', blank=True)
    passengers_count = models.PositiveIntegerField(default=1)
    duration = models.CharField(max_length=30, choices=DURATION_CHOICES, null=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, null=True, blank=True)
    price = models.PositiveIntegerField(default=1, null=True, blank=True)
    tag = models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.title

    

class TopActivities(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=800)  
    image = models.ImageField(upload_to='top_activities/')

    def __str__(self):
        return self.name
