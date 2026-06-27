from django.db import models
from django.conf import settings
from apps.accounts.models import Child
from apps.dashboard.models import Event


class EventRsvp(models.Model):
    STATUS_ATTENDING = 'attending'
    STATUS_NOT_ATTENDING = 'not_attending'
    STATUS_CHOICES = [
        (STATUS_ATTENDING, '参加'),
        (STATUS_NOT_ATTENDING, '不参加'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_rsvps')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user')


class AbsenceReport(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='absence_reports')
    date = models.DateField()
    reason = models.TextField(blank=True)
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='absence_reports'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('child', 'date')

    def __str__(self):
        return f"{self.child} - {self.date}"


class Submission(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_SUBMITTED = 'submitted'
    STATUS_ACCEPTED = 'accepted'
    STATUS_CHOICES = [
        (STATUS_PENDING, '提出待ち'),
        (STATUS_SUBMITTED, '提出済'),
        (STATUS_ACCEPTED, '受理済'),
    ]

    title_ja = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    due_date = models.DateField(null=True, blank=True)
    parent = models.ForeignKey('accounts.Parent', on_delete=models.CASCADE, related_name='submissions')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title_ja


class Survey(models.Model):
    title_ja = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    options_ja = models.JSONField(default=list)
    options_en = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_ja


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_responses')
    choice_index = models.PositiveSmallIntegerField()
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('survey', 'user')
