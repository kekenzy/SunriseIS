from django.urls import path
from .views import (
    ParentEventListView, EventRsvpView,
    AbsenceReportCreateView, SubmissionListView, SubmissionUpdateView,
    SurveyListView, SurveyAnswerView,
)

parent_urlpatterns = [
    path('events/', ParentEventListView.as_view(), name='parent-events-v2'),
    path('events/<int:pk>/rsvp/', EventRsvpView.as_view(), name='parent-event-rsvp'),
    path('absence/', AbsenceReportCreateView.as_view(), name='parent-absence'),
    path('submissions/', SubmissionListView.as_view(), name='parent-submissions'),
    path('submissions/<int:pk>/submit/', SubmissionUpdateView.as_view(), name='parent-submission-submit'),
    path('surveys/', SurveyListView.as_view(), name='parent-surveys'),
    path('surveys/<int:pk>/answer/', SurveyAnswerView.as_view(), name='parent-survey-answer'),
]
