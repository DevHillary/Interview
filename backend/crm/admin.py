from django.contrib import admin
from .models import Lead, Contact, Note, Reminder, Correspondence, AuditLog


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'email', 'status', 'priority', 'owner', 'created_at']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['name', 'company', 'email', 'phone']
    date_hierarchy = 'created_at'
    raw_id_fields = ['owner']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'lead', 'position', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['name', 'email', 'phone']
    date_hierarchy = 'created_at'
    raw_id_fields = ['lead']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['lead', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
    date_hierarchy = 'created_at'
    raw_id_fields = ['lead', 'author']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['title', 'lead', 'user', 'reminder_date', 'status', 'is_overdue']
    list_filter = ['status', 'reminder_date', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'reminder_date'
    raw_id_fields = ['lead', 'user']


@admin.register(Correspondence)
class CorrespondenceAdmin(admin.ModelAdmin):
    list_display = ['subject', 'contact', 'type', 'date', 'logged_by']
    list_filter = ['type', 'date', 'created_at']
    search_fields = ['subject', 'description']
    date_hierarchy = 'date'
    raw_id_fields = ['contact', 'logged_by']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_id', 'object_repr', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['object_repr', 'user__username']
    date_hierarchy = 'timestamp'
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'timestamp', 'ip_address']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False



