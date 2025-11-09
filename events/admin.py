from django.contrib import admin
from .models import EventCategory, Event, Registration

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_editable = ('color',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'category', 'date', 'location', 'registered_count', 'spots_available')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description', 'location')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registered_at')
    list_filter = ('event', 'registered_at')