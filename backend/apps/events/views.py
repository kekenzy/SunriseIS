from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from apps.dashboard.models import Event
from apps.accounts.models import Child
from .models import EventRsvp, AbsenceReport, Submission, Survey, SurveyResponse
from .serializers import (
    EventWithRsvpSerializer, EventRsvpSerializer,
    AbsenceReportSerializer, SubmissionSerializer, SurveySerializer
)


class ParentEventListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventWithRsvpSerializer

    def get_queryset(self):
        today = timezone.localdate()
        return Event.objects.filter(event_date__gte=today)


class EventRsvpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'detail': 'イベントが見つかりません。'}, status=404)

        rsvp_status = request.data.get('status')
        if rsvp_status not in (EventRsvp.STATUS_ATTENDING, EventRsvp.STATUS_NOT_ATTENDING):
            return Response({'detail': '無効なステータスです。'}, status=400)

        rsvp, _ = EventRsvp.objects.update_or_create(
            event=event, user=request.user,
            defaults={'status': rsvp_status}
        )
        return Response(EventRsvpSerializer(rsvp).data)


class AbsenceReportCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            parent = request.user.parent_profile
            child = parent.children.first()
        except Exception:
            return Response({'detail': '保護者プロフィールが見つかりません。'}, status=404)

        if not child:
            return Response({'detail': 'お子さまが登録されていません。'}, status=404)

        date = request.data.get('date')
        reason = request.data.get('reason', '')

        if not date:
            return Response({'detail': '日付は必須です。'}, status=400)

        report, created = AbsenceReport.objects.get_or_create(
            child=child, date=date,
            defaults={'reason': reason, 'reported_by': request.user}
        )
        if not created:
            report.reason = reason
            report.save()

        return Response(AbsenceReportSerializer(report).data, status=201 if created else 200)


class SubmissionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        try:
            return self.request.user.parent_profile.submissions.all()
        except Exception:
            return Submission.objects.none()


class SubmissionUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            submission = request.user.parent_profile.submissions.get(pk=pk, status=Submission.STATUS_PENDING)
        except Submission.DoesNotExist:
            return Response({'detail': '申請が見つかりません。'}, status=404)

        submission.status = Submission.STATUS_SUBMITTED
        submission.submitted_at = timezone.now()
        submission.save()
        return Response(SubmissionSerializer(submission).data)


class SurveyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()


class SurveyAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            survey = Survey.objects.get(pk=pk)
        except Survey.DoesNotExist:
            return Response({'detail': 'アンケートが見つかりません。'}, status=404)

        try:
            choice_index = int(request.data.get('choice_index', ''))
        except (TypeError, ValueError):
            return Response({'detail': '選択肢インデックスは整数で指定してください。'}, status=400)

        if choice_index < 0 or choice_index >= len(survey.options_ja):
            return Response({'detail': '無効な選択肢です。'}, status=400)

        SurveyResponse.objects.update_or_create(
            survey=survey, user=request.user,
            defaults={'choice_index': choice_index}
        )
        return Response({'detail': '回答しました。', 'choice_index': choice_index})
