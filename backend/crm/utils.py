from .models import AuditLog


def log_model_change(user, action, instance, changes=None, request=None):
    """
    Utility function to log model changes to the audit trail.
    
    Args:
        user: The user who made the change
        action: The action performed (create, update, delete)
        instance: The model instance that was changed
        changes: Dictionary of field changes (for updates)
        request: The HTTP request object (to get IP address)
    """
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=instance.__class__.__name__,
        object_id=instance.id,
        object_repr=str(instance),
        changes=changes or {},
        ip_address=ip_address
    )



