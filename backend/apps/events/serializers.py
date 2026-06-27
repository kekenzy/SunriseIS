from rest_framework import serializers
from apps.dashboard.models import Event
from .models import EventRsvp, AbsenceReport, Submission, Survey, SurveyResponse


class EventWithRsvpSerializer(serializers.ModelSerializer):
    rsvp_status = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title_ja', 'title_en', 'event_date', 'time_range', 'place', 'rsvp_status']

    def get_rsvp_status(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        rsvp = obj.rsvps.filter(user=request.user).first()
        return rsvp.status if rsvp else None


class EventRsvpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRsvp
        fields = ['id', 'status', 'answered_at']


class AbsenceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceReport
        fields = ['id', 'child', 'date', 'reason', 'created_at']
        read_only_fields = ['created_at']


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'title_ja', 'title_en', 'due_date', 'status', 'submitted_at']


class SurveySerializer(serializers.ModelSerializer):
    my_response = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ['id', 'title_ja', 'title_en', 'options_ja', 'options_en', 'my_response']

    def get_my_response(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        resp = obj.responses.filter(user=request.user).first()
        return resp.choice_index if resp else None
