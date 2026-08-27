from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Service, Appointment

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price')
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('customer__username', 'service__name')