from django.contrib import admin
from .models import TourBooking,TransferBooking

@admin.register(TourBooking)
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


from django.contrib.auth import get_user_model

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import path


@admin.register(TransferBooking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'status', 'transfer_name', 'get_driver_username')
    list_filter = ('status', 'date', 'driver')
    search_fields = ('name', 'email')
    actions = ['reject_bookings', 'assign_driver']

    def get_driver_username(self, obj):
        return obj.driver.username if obj.driver else '-'
    get_driver_username.short_description = 'Driver'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('assign-driver/', self.assign_driver_view, name='assign-driver'),
        ]
        return custom_urls + urls

    def assign_driver(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(f"assign-driver/?ids={','.join(selected)}")
    assign_driver.short_description = "Assign driver to selected bookings"

    def assign_driver_view(self, request):
        if request.method == 'POST':
            driver_id = request.POST.get('driver')
            ids = request.GET.get('ids').split(',')
            driver = get_user_model().objects.get(id=driver_id)
            updated = TransferBooking.objects.filter(id__in=ids).update(driver=driver)
            self.message_user(request, f'{updated} bookings were assigned to {driver.username}.')
            return HttpResponseRedirect("../")

        drivers = get_user_model().objects.filter(groups__name='Driver').order_by('username')
        context = {
            'title': 'Assign Driver to Bookings',
            'drivers': drivers,
            'opts': self.model._meta,
        }
        return self.admin_site.render(request, 'admin/assign_driver.html', context)

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