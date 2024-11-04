from django.db import models
from django.utils import timezone


class TourImage(models.Model):
    image = models.ImageField(upload_to='tours/')
    alt_text = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.alt_text if self.alt_text else "Tour Image"


class ToursAndActivities(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=3000)
    media_gallery = models.ManyToManyField(TourImage, related_name='tours',blank=True)
    passengers_count = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=1,null=True,blank=True)

    def __str__(self):
        return self.title
    

class TopActivities(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=800)  
    image = models.ImageField(upload_to='top_activities/')

    def __str__(self):
        return self.name
