from django.db import models

class BackgroundVideo(models.Model):
    video = models.FileField(upload_to='videos/')
    
    def __str__(self):
        return "Background Video"

class CardOne(models.Model):
    image1 = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=400)
    
    def __str__(self):
        return self.title

class CardTwo(models.Model):
    image2 = models.ImageField(upload_to='images/')
    title2 = models.CharField(max_length=255)
    description = models.TextField(max_length=400)
    
    def __str__(self):
        return self.title2
