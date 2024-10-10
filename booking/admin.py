from django.contrib import admin
from .models import Booking,TransferBooking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'status','tour_activity')
    list_filter = ('status', 'date')
    search_fields = ('name', 'email')
    actions = ['reject_bookings']

    def reject_bookings(self, request, queryset):
        for booking in queryset:
            booking.status = 'rejected'
            booking.save()
        self.message_user(request, f"{queryset.count()} booking(s) have been rejected.")
    reject_bookings.short_description = "Reject selected bookings"

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status == 'rejected':
            reason = request.POST.get('rejection_reason')
            if reason:
                obj.rejection_reason = reason
                obj.save()
            else:
                self.message_user(request, "Please provide a reason for rejection.", level='error')
                return
        super().save_model(request, obj, form, change)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_rejection_reason'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    class Media:
        js = ('admin/js/booking_admin.js',)




@admin.register(TransferBooking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'status','transfer_name')
    list_filter = ('status', 'date')
    search_fields = ('name', 'email')
    actions = ['reject_bookings']

    def reject_bookings(self, request, queryset):
        for booking in queryset:
            booking.status = 'rejected'
            booking.save()
        self.message_user(request, f"{queryset.count()} booking(s) have been rejected.")
    reject_bookings.short_description = "Reject selected bookings"

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status == 'rejected':
            reason = request.POST.get('rejection_reason')
            if reason:
                obj.rejection_reason = reason
                obj.save()
            else:
                self.message_user(request, "Please provide a reason for rejection.", level='error')
                return
        super().save_model(request, obj, form, change)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_rejection_reason'] = True
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    class Media:
        js = ('admin/js/booking_admin.js',)