# admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from .models import TransferMeetAssist, Point

class PointInline(admin.TabularInline):
    model = Point
    extra = 1

@admin.register(TransferMeetAssist)
class TransferMeetAssistAdmin(admin.ModelAdmin):
    inlines = [PointInline]
    list_display = ['name', 'cost', 'image_preview']
    search_fields = ['name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

admin.site.register(Point)


# admin.site.unregister(User)
admin.site.unregister(Group)
