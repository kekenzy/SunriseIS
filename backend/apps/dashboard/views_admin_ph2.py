from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsAdminOrStaff
from apps.accounts.models import Child
from apps.accounts.serializers import ChildSerializer


class AdminStudentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    serializer_class = ChildSerializer

    def get_queryset(self):
        qs = Child.objects.select_related('parent__user').all()
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(name_ja__icontains=q) | qs.filter(class_name__icontains=q)
        return qs
