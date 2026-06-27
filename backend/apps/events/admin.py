from django.contrib import admin
from .models import EventRsvp, AbsenceReport, Submission, Survey, SurveyResponse


@admin.register(EventRsvp)
class EventRsvpAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'status', 'answered_at']


@admin.register(AbsenceReport)
class AbsenceReportAdmin(admin.ModelAdmin):
    list_display = ['child', 'date', 'reported_by', 'created_at']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['title_ja', 'parent', 'status', 'due_date']
    list_filter = ['status']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title_ja', 'created_at']


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['survey', 'user', 'choice_index', 'answered_at']
