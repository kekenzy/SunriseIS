from django.urls import path
from .views import ParentBillListView, ParentBillPayView, ParentReceiptView, AdminBillListView

parent_urlpatterns = [
    path('bills/', ParentBillListView.as_view(), name='parent-bills'),
    path('bills/<int:pk>/pay/', ParentBillPayView.as_view(), name='parent-bill-pay'),
    path('bills/<int:pk>/receipt/', ParentReceiptView.as_view(), name='parent-receipt'),
]

admin_urlpatterns = [
    path('bills/', AdminBillListView.as_view(), name='admin-bills'),
]
