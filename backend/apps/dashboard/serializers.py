from rest_framework import serializers
from .models import Attendance, Event
from apps.accounts.models import Child


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'date', 'status']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title_ja', 'title_en', 'event_date', 'time_range', 'place']


class ChildAttendanceSerializer(serializers.ModelSerializer):
    attendance_records = AttendanceSerializer(many=True, read_only=True)

    class Meta:
        model = Child
        fields = ['id', 'name_ja', 'name_en', 'class_name', 'attendance_records']
