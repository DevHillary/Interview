from rest_framework import serializers
from .models import Lead, Contact, Note, Reminder, Correspondence, AuditLog
from users.serializers import UserSerializer


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""
    
    class Meta:
        model = Contact
        fields = ['id', 'lead', 'name', 'email', 'phone', 'position', 'is_primary', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model."""
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Note
        fields = ['id', 'lead', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReminderSerializer(serializers.ModelSerializer):
    """Serializer for Reminder model."""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Reminder
        fields = ['id', 'lead', 'user', 'user_id', 'title', 'description', 'reminder_date', 'status', 'is_overdue', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CorrespondenceSerializer(serializers.ModelSerializer):
    """Serializer for Correspondence model."""
    logged_by = UserSerializer(read_only=True)
    logged_by_id = serializers.IntegerField(write_only=True, required=False)
    contact_name = serializers.CharField(source='contact.name', read_only=True)
    
    class Meta:
        model = Correspondence
        fields = ['id', 'contact', 'contact_name', 'type', 'subject', 'description', 'date', 'logged_by', 'logged_by_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead model."""
    owner = UserSerializer(read_only=True)
    owner_id = serializers.IntegerField(write_only=True, required=False)
    contacts = ContactSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    reminders = ReminderSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'company', 'email', 'phone', 'status', 'priority', 
            'source', 'owner', 'owner_id', 'estimated_value', 'description',
            'contacts', 'notes', 'reminders', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LeadListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing leads."""
    owner = UserSerializer(read_only=True)
    contacts_count = serializers.IntegerField(source='contacts.count', read_only=True)
    notes_count = serializers.IntegerField(source='notes.count', read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'company', 'email', 'phone', 'status', 'priority',
            'owner', 'estimated_value', 'contacts_count', 'notes_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AuditLog model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'timestamp', 'ip_address']
        read_only_fields = ['id', 'timestamp']

