from django.contrib import admin
from .models import Statistic, Activity,Description
from django.utils.html import format_html


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('title', 'value')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_display')
    search_fields = ('name',)
    
    def icon_display(self, obj):
        return format_html('<div style="width: 24px; height: 24px;">{}</div>', obj.icon)
    icon_display.short_description = 'Icon'

# admin.site.register(Description)
