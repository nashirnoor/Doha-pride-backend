from django.contrib import admin
from .models import DriverFeedback,Banner,User

@admin.register(DriverFeedback)
class DriverFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_driver_name', 'description', 'get_image')
    list_display_links = ('id', 'get_driver_name')
    search_fields = ('user__username', 'user__email', 'description')

    def get_driver_name(self, obj):
        if obj.user:
            return obj.user.username
        return 'No User'
    get_driver_name.short_description = 'Driver Name'

    def get_image(self, obj):
        if obj.image:
            return 'Yes'
        return 'No'
    get_image.short_description = 'Has Image'

admin.site.register(Banner)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type') 
    search_fields = ('email', 'username')  
    list_filter = ('user_type',)  

admin.site.register(User, UserAdmin)
