from django.db import models

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('Destination Guide', 'Destination Guide'),
        ('Food & Culture', 'Food & Culture'),
        ('Adventure Travel', 'Adventure Travel'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    read_time = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title