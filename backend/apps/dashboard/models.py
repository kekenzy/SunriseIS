from django.db import models
from apps.accounts.models import Child


class Attendance(models.Model):
    STATUS_PRESENT = 'present'
    STATUS_ABSENT = 'absent'
    STATUS_EVENT = 'event'
    STATUS_CHOICES = [
        (STATUS_PRESENT, '出席'),
        (STATUS_ABSENT, '欠席'),
        (STATUS_EVENT, '行事'),
    ]

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PRESENT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('child', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.child} - {self.date} - {self.status}"


class Event(models.Model):
    title_ja = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    event_date = models.DateField()
    time_range = models.CharField(max_length=50, blank=True)
    place = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title_ja
