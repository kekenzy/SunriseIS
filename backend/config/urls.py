from django.contrib import admin
from django.urls import path, include
from apps.billing.urls import parent_urlpatterns as billing_parent_urls, admin_urlpatterns as billing_admin_urls
from apps.events.urls import parent_urlpatterns as events_parent_urls
from apps.dashboard.views_admin_ph2 import AdminStudentListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/parent/', include('apps.dashboard.urls_parent')),
    path('api/parent/', include(billing_parent_urls)),
    path('api/parent/', include(events_parent_urls)),
    path('api/admin/', include('apps.dashboard.urls_admin')),
    path('api/admin/', include(billing_admin_urls)),
    path('api/admin/students/', AdminStudentListView.as_view(), name='admin-students'),
]
