from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LeadViewSet, ContactViewSet, NoteViewSet, 
    ReminderViewSet, CorrespondenceViewSet, AuditLogViewSet,
    dashboard_stats, export_leads_csv
)

router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'reminders', ReminderViewSet, basename='reminder')
router.register(r'correspondences', CorrespondenceViewSet, basename='correspondence')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    path('leads/export/csv/', export_leads_csv, name='export-leads-csv'),
]


