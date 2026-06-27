from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsAdminOrStaff
from rest_framework.views import APIView
from django.db.models import Q
from .models import Notice, NoticeRead
from .serializers import NoticeSerializer, NoticeCreateSerializer


class ParentNoticeListView(generics.ListAPIView):
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notice.objects.filter(
            Q(target_role='all') | Q(target_role='parent')
        )


class ParentNoticeDetailView(generics.RetrieveAPIView):
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notice.objects.filter(
            Q(target_role='all') | Q(target_role='parent')
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        NoticeRead.objects.get_or_create(notice=instance, user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AdminNoticeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get_queryset(self):
        return Notice.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NoticeCreateSerializer
        return NoticeSerializer


class AdminNoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return NoticeCreateSerializer
        return NoticeSerializer
