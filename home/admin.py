# admin.py
from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'read_time')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'