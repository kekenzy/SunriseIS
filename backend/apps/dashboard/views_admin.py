from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsAdminOrStaff
from django.utils import timezone
from apps.accounts.models import User, Child
from apps.notices.models import Notice
from .models import Attendance


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get(self, request):
        today = timezone.localdate()

        total_children = Child.objects.count()

        today_attendance = Attendance.objects.filter(date=today)
        present_count = today_attendance.filter(status='present').count()
        absent_count = today_attendance.filter(status='absent').count()
        not_recorded = total_children - today_attendance.count()

        total_notices = Notice.objects.count()

        return Response({
            'total_children': total_children,
            'today_attendance': {
                'present': present_count,
                'absent': absent_count,
                'not_recorded': max(not_recorded, 0),
            },
            'total_notices': total_notices,
        })
