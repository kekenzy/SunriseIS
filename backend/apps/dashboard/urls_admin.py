from django.urls import path
from .views_admin import AdminDashboardView
from apps.notices.views import AdminNoticeListCreateView, AdminNoticeDetailView

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('notices/', AdminNoticeListCreateView.as_view(), name='admin-notices'),
    path('notices/<int:pk>/', AdminNoticeDetailView.as_view(), name='admin-notice-detail'),
]
