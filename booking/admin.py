from django.contrib import admin
# import django_filters
from .models import *
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
@admin.register(Booking)
class BookingAdmin(SummernoteModelAdmin):
    list_filter = ('status', 'day')
    list_display = ('table', 'status', 'day')
    search_fields = ['day']
# class BookingFilter(django_filters.FilterSet):
#     """Filter for bookings rendered in profile page"""
#     class Meta:
#         model = Booking
#         fields = ['date', 'start_time', 'end_time', 'table',
#                   'customer_full_name', 'created_by']