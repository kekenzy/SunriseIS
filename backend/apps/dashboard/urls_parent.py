from django.urls import path
from .views_parent import (
    ParentDashboardView, ParentChildrenView,
    ParentAttendanceView, ParentEventListView
)
from apps.notices.views import ParentNoticeListView, ParentNoticeDetailView

urlpatterns = [
    path('dashboard/', ParentDashboardView.as_view(), name='parent-dashboard'),
    path('children/', ParentChildrenView.as_view(), name='parent-children'),
    path('attendance/', ParentAttendanceView.as_view(), name='parent-attendance'),
    path('events/', ParentEventListView.as_view(), name='parent-events'),
    path('notices/', ParentNoticeListView.as_view(), name='parent-notices'),
    path('notices/<int:pk>/', ParentNoticeDetailView.as_view(), name='parent-notice-detail'),
]
