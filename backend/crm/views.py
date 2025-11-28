from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import csv
from .models import Lead, Contact, Note, Reminder, Correspondence, AuditLog
from .serializers import (
    LeadSerializer, LeadListSerializer, ContactSerializer, 
    NoteSerializer, ReminderSerializer, CorrespondenceSerializer, AuditLogSerializer
)
from .permissions import IsManagerOrReadOnly
from .utils import log_model_change


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lead model with CRUD operations.
    Supports filtering by status, owner, and date.
    """
    queryset = Lead.objects.all().select_related('owner').prefetch_related('contacts', 'notes', 'reminders')
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'owner']
    search_fields = ['name', 'company', 'email', 'phone', 'description']
    ordering_fields = ['created_at', 'updated_at', 'estimated_value', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LeadListSerializer
        return LeadSerializer
    
    @swagger_auto_schema(
        operation_description="Create a new lead in the CRM system",
        request_body=LeadSerializer,
        responses={
            201: openapi.Response(
                description="Lead created successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "name": "John Kamau",
                        "company": "Safaricom Ltd",
                        "email": "j.kamau@safaricom.co.ke",
                        "phone": "+254-722-123-456",
                        "status": "new",
                        "priority": "high",
                        "source": "Website",
                        "estimated_value": "2500000.00",
                        "description": "Interested in enterprise CRM solution"
                    }
                }
            ),
            400: "Bad Request - Invalid data"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Set the current user as owner if not specified
        if not serializer.validated_data.get('owner_id'):
            serializer.save(owner=self.request.user)
        else:
            serializer.save()
        # Log the creation
        log_model_change(
            user=self.request.user,
            action='create',
            instance=serializer.instance,
            request=self.request
        )
    
    def perform_update(self, serializer):
        old_instance = self.get_object()
        # Track changes
        changes = {}
        for field in ['name', 'company', 'status', 'priority', 'estimated_value']:
            old_value = getattr(old_instance, field)
            new_value = serializer.validated_data.get(field, old_value)
            if old_value != new_value:
                changes[field] = {'old': str(old_value), 'new': str(new_value)}
        
        serializer.save()
        
        # Log the update
        log_model_change(
            user=self.request.user,
            action='update',
            instance=serializer.instance,
            changes=changes,
            request=self.request
        )
    
    def perform_destroy(self, instance):
        # Log the deletion
        log_model_change(
            user=self.request.user,
            action='delete',
            instance=instance,
            request=self.request
        )
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def audit_log(self, request, pk=None):
        """Get audit log for a specific lead."""
        lead = self.get_object()
        logs = AuditLog.objects.filter(model_name='Lead', object_id=lead.id)
        serializer = AuditLogSerializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_leads(self, request):
        """Get leads owned by the current user."""
        leads = self.queryset.filter(owner=request.user)
        page = self.paginate_queryset(leads)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(leads, many=True)
        return Response(serializer.data)


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Contact model with CRUD operations.
    """
    queryset = Contact.objects.all().select_related('lead')
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lead', 'is_primary']
    search_fields = ['name', 'email', 'phone', 'position']
    ordering_fields = ['created_at', 'name']
    ordering = ['-is_primary', 'name']
    
    def perform_create(self, serializer):
        serializer.save()
        # Log the creation
        log_model_change(
            user=self.request.user,
            action='create',
            instance=serializer.instance,
            request=self.request
        )
    
    def perform_update(self, serializer):
        old_instance = self.get_object()
        # Track changes
        changes = {}
        for field in ['name', 'email', 'phone', 'position', 'is_primary']:
            old_value = getattr(old_instance, field)
            new_value = serializer.validated_data.get(field, old_value)
            if old_value != new_value:
                changes[field] = {'old': str(old_value), 'new': str(new_value)}
        
        serializer.save()
        
        # Log the update
        log_model_change(
            user=self.request.user,
            action='update',
            instance=serializer.instance,
            changes=changes,
            request=self.request
        )
    
    def perform_destroy(self, instance):
        # Log the deletion
        log_model_change(
            user=self.request.user,
            action='delete',
            instance=instance,
            request=self.request
        )
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def correspondences(self, request, pk=None):
        """Get all correspondences for a specific contact."""
        contact = self.get_object()
        correspondences = contact.correspondences.all()
        serializer = CorrespondenceSerializer(correspondences, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def audit_log(self, request, pk=None):
        """Get audit log for a specific contact."""
        contact = self.get_object()
        logs = AuditLog.objects.filter(model_name='Contact', object_id=contact.id)
        serializer = AuditLogSerializer(logs, many=True)
        return Response(serializer.data)


class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Note model with CRUD operations.
    """
    queryset = Note.objects.all().select_related('lead', 'author')
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lead', 'author']
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        # Set the current user as author
        serializer.save(author=self.request.user)


class ReminderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Reminder model with CRUD operations.
    """
    queryset = Reminder.objects.all().select_related('lead', 'user')
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['lead', 'user', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['reminder_date', 'created_at']
    ordering = ['reminder_date']
    
    def perform_create(self, serializer):
        # Set the current user if not specified
        if not serializer.validated_data.get('user_id'):
            serializer.save(user=self.request.user)
        else:
            serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_reminders(self, request):
        """Get reminders for the current user."""
        reminders = self.queryset.filter(user=request.user, status='pending')
        page = self.paginate_queryset(reminders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(reminders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue reminders."""
        reminders = self.queryset.filter(
            status='pending',
            reminder_date__lt=timezone.now()
        )
        page = self.paginate_queryset(reminders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(reminders, many=True)
        return Response(serializer.data)


class CorrespondenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Correspondence model with CRUD operations.
    """
    queryset = Correspondence.objects.all().select_related('contact', 'logged_by')
    serializer_class = CorrespondenceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['contact', 'type', 'logged_by']
    search_fields = ['subject', 'description']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    
    def perform_create(self, serializer):
        # Set the current user as logged_by
        serializer.save(logged_by=self.request.user)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for AuditLog model (read-only).
    """
    queryset = AuditLog.objects.all().select_related('user')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'action', 'model_name']
    search_fields = ['object_repr']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for the current user.
    Returns counts, values, and distributions of leads.
    """
    # Get all leads for statistics
    all_leads = Lead.objects.all()
    user_leads = all_leads.filter(owner=request.user)
    
    # Basic counts
    total_leads = all_leads.count()
    user_total_leads = user_leads.count()
    
    # Status distribution
    status_distribution = dict(
        all_leads.values('status')
        .annotate(count=Count('id'))
        .values_list('status', 'count')
    )
    
    # Priority distribution
    priority_distribution = dict(
        all_leads.values('priority')
        .annotate(count=Count('id'))
        .values_list('priority', 'count')
    )
    
    # Calculate total estimated value
    total_value = all_leads.aggregate(
        total=Sum('estimated_value')
    )['total'] or 0
    
    user_total_value = user_leads.aggregate(
        total=Sum('estimated_value')
    )['total'] or 0
    
    # Recent activity (last 10 audit logs)
    recent_activity = AuditLog.objects.select_related('user').order_by('-timestamp')[:10]
    recent_activity_data = [{
        'id': log.id,
        'user': log.user.username if log.user else 'System',
        'action': log.get_action_display(),
        'model': log.model_name,
        'object': log.object_repr,
        'timestamp': log.timestamp
    } for log in recent_activity]
    
    # Upcoming reminders
    upcoming_reminders = Reminder.objects.filter(
        user=request.user,
        status='pending',
        reminder_date__gte=timezone.now()
    ).order_by('reminder_date')[:5]
    
    upcoming_reminders_data = [{
        'id': reminder.id,
        'title': reminder.title,
        'lead': reminder.lead.name,
        'date': reminder.reminder_date
    } for reminder in upcoming_reminders]
    
    # Overdue reminders count
    overdue_reminders_count = Reminder.objects.filter(
        user=request.user,
        status='pending',
        reminder_date__lt=timezone.now()
    ).count()
    
    stats = {
        'total_leads': total_leads,
        'user_total_leads': user_total_leads,
        'new_leads': status_distribution.get('new', 0),
        'contacted_leads': status_distribution.get('contacted', 0),
        'qualified_leads': status_distribution.get('qualified', 0),
        'converted_leads': status_distribution.get('converted', 0),
        'lost_leads': status_distribution.get('lost', 0),
        'total_value': float(total_value),
        'user_total_value': float(user_total_value),
        'status_distribution': status_distribution,
        'priority_distribution': priority_distribution,
        'recent_activity': recent_activity_data,
        'upcoming_reminders': upcoming_reminders_data,
        'overdue_reminders_count': overdue_reminders_count,
        'total_contacts': Contact.objects.count(),
        'total_notes': Note.objects.count(),
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_leads_csv(request):
    """
    Export leads to CSV format.
    """
    # Get filtered leads based on query parameters
    leads = Lead.objects.all().select_related('owner')
    
    # Apply filters if provided
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    owner = request.GET.get('owner')
    
    if status:
        leads = leads.filter(status=status)
    if priority:
        leads = leads.filter(priority=priority)
    if owner:
        leads = leads.filter(owner_id=owner)
    
    # Create HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="leads_export.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow([
        'ID',
        'Name',
        'Company',
        'Email',
        'Phone',
        'Status',
        'Priority',
        'Source',
        'Owner',
        'Estimated Value (KES)',
        'Description',
        'Created Date',
        'Last Updated'
    ])
    
    # Write data rows
    for lead in leads:
        writer.writerow([
            lead.id,
            lead.name,
            lead.company,
            lead.email,
            lead.phone,
            lead.get_status_display(),
            lead.get_priority_display(),
            lead.source,
            lead.owner.username if lead.owner else 'N/A',
            lead.estimated_value if lead.estimated_value else 0,
            lead.description,
            lead.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            lead.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response


