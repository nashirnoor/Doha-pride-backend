from django.db import models


class HomeBanner(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='banners/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title or f"Banner {self.id}"
    

class TransferMeetAssist(models.Model):
    name = models.CharField(max_length=255)
    description_one = models.TextField()
    description_two = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='transfer_meet_assist/', null=True, blank=True)

    def __str__(self):
        return self.name
    

class Point(models.Model):
    transfer_meet_assist = models.ForeignKey(TransferMeetAssist, related_name='points', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text