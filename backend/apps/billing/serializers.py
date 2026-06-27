from rest_framework import serializers
from .models import Bill, Receipt


class BillSerializer(serializers.ModelSerializer):
    has_receipt = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = ['id', 'month', 'description_ja', 'description_en',
                  'amount', 'status', 'due_date', 'paid_at', 'has_receipt']

    def get_has_receipt(self, obj):
        return hasattr(obj, 'receipt')


class ReceiptSerializer(serializers.ModelSerializer):
    bill = BillSerializer(read_only=True)

    class Meta:
        model = Receipt
        fields = ['id', 'bill', 'issued_at']
