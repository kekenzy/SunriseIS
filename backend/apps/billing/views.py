from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsAdminOrStaff
from django.utils import timezone
from .models import Bill, Receipt
from .serializers import BillSerializer, ReceiptSerializer


class ParentBillListView(generics.ListAPIView):
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            return self.request.user.parent_profile.bills.all()
        except Exception:
            return Bill.objects.none()


class ParentBillPayView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            bill = request.user.parent_profile.bills.get(pk=pk, status=Bill.STATUS_UNPAID)
        except Bill.DoesNotExist:
            return Response({'detail': '請求が見つかりません。'}, status=404)

        bill.status = Bill.STATUS_PAID
        bill.paid_at = timezone.now()
        bill.save()
        Receipt.objects.get_or_create(bill=bill)
        return Response(BillSerializer(bill).data)


class ParentReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            bill = request.user.parent_profile.bills.get(pk=pk, status=Bill.STATUS_PAID)
            receipt = bill.receipt
        except (Bill.DoesNotExist, Receipt.DoesNotExist):
            return Response({'detail': '領収書が見つかりません。'}, status=404)
        return Response(ReceiptSerializer(receipt).data)


class AdminBillListView(generics.ListAPIView):
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    queryset = Bill.objects.select_related('parent__user').all()
