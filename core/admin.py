from django.contrib import admin
from .models import Category, MenuItem, Booking, Lead

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Lead)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_id', 'name', 'date', 'time_slot', 'guests')
    list_filter = ('date',)
    search_fields = ('name', 'reference_id')