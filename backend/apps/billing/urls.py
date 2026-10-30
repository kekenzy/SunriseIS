from django.urls import path
from .views import ParentBillListView, ParentReceiptView, AdminBillListView, AdminBillMarkPaidView

parent_urlpatterns = [
    path('bills/', ParentBillListView.as_view(), name='parent-bills'),
    path('bills/<int:pk>/receipt/', ParentReceiptView.as_view(), name='parent-receipt'),
]

admin_urlpatterns = [
    path('bills/', AdminBillListView.as_view(), name='admin-bills'),
    path('bills/<int:pk>/mark-paid/', AdminBillMarkPaidView.as_view(), name='admin-bill-mark-paid'),
]
