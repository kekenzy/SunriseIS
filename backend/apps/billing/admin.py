from django.contrib import admin
from .models import Bill, Receipt


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['parent', 'month', 'description_ja', 'amount', 'status', 'due_date']
    list_filter = ['status', 'month']


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['bill', 'issued_at']
