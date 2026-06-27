from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.utils import timezone
from django.db.models import Q
from apps.accounts.models import Child
from apps.accounts.serializers import ChildSerializer
from apps.notices.models import Notice, NoticeRead
from .models import Attendance, Event
from .serializers import AttendanceSerializer, EventSerializer


class ParentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            parent = user.parent_profile
            children = parent.children.all()
        except Exception:
            return Response({'detail': '保護者プロフィールが見つかりません。'}, status=404)

        today = timezone.localdate()
        first_child = children.first()

        # 今月の出席率
        attendance_summary = {}
        if first_child:
            this_month = today.replace(day=1)
            records = Attendance.objects.filter(
                child=first_child,
                date__gte=this_month,
                date__lte=today
            )
            present_days = records.filter(status='present').count()
            total_days = records.exclude(status='absent').count() + records.filter(status='absent').count()
            attendance_summary = {
                'present': present_days,
                'total': total_days,
                'rate': round(present_days / total_days * 100) if total_days > 0 else 0,
            }

        # 未読お知らせ数
        visible_notices = Notice.objects.filter(
            Q(target_role='all') | Q(target_role='parent')
        )
        read_ids = NoticeRead.objects.filter(user=user).values_list('notice_id', flat=True)
        unread_count = visible_notices.exclude(id__in=read_ids).count()

        # 直近イベント
        upcoming_events = Event.objects.filter(event_date__gte=today)[:3]

        return Response({
            'parent_name': parent.name_ja,
            'children': ChildSerializer(children, many=True).data,
            'attendance': attendance_summary,
            'unread_notices': unread_count,
            'upcoming_events': EventSerializer(upcoming_events, many=True).data,
        })


class ParentChildrenView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChildSerializer

    def get_queryset(self):
        try:
            return self.request.user.parent_profile.children.all()
        except Exception:
            return Child.objects.none()


class ParentAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            parent = request.user.parent_profile
            child = parent.children.first()
        except Exception:
            return Response({'detail': '保護者プロフィールが見つかりません。'}, status=404)

        if not child:
            return Response({'records': []})

        today = timezone.localdate()
        year = int(request.query_params.get('year', today.year))
        month = int(request.query_params.get('month', today.month))

        records = Attendance.objects.filter(
            child=child,
            date__year=year,
            date__month=month
        )
        return Response({
            'child': ChildSerializer(child).data,
            'year': year,
            'month': month,
            'records': AttendanceSerializer(records, many=True).data,
        })


class ParentEventListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get_queryset(self):
        today = timezone.localdate()
        return Event.objects.filter(event_date__gte=today)
