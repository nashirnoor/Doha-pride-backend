from django.db import models

class Statistic(models.Model):
    title = models.CharField(max_length=255)
    value = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title}: {self.value}"

class Activity(models.Model):
    name = models.CharField(max_length=155)
    icon = models.CharField(max_length=555)  

    def __str__(self):
        return self.name
    
class Description(models.Model):
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.description
