from django.contrib import admin
from .models import Attendance, Event


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['child', 'date', 'status']
    list_filter = ['status', 'date']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title_ja', 'event_date', 'place']
