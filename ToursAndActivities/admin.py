from django.contrib import admin
from .models import ToursAndActivities, TourImage, TopActivities
from django.utils.html import format_html


class TourImageInline(admin.TabularInline):
    model = ToursAndActivities.media_gallery.through
    extra = 1

@admin.register(ToursAndActivities)
class ToursAndActivitiesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    inlines = [TourImageInline]
    filter_horizontal = ('media_gallery',)

@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'alt_text')
    search_fields = ('alt_text',)


class TopActivitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image_preview')
    search_fields = ('name',)
    list_filter = ('name',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'


admin.site.register(TopActivities, TopActivitiesAdmin)
