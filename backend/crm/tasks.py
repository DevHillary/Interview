from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Reminder


@shared_task
def check_reminders():
    """
    Celery task to check for due reminders and send notifications.
    This task runs periodically to check for reminders that need to be sent.
    """
    now = timezone.now()
    
    # Get all pending reminders that are due
    due_reminders = Reminder.objects.filter(
        status='pending',
        reminder_date__lte=now
    ).select_related('user', 'lead')
    
    count = 0
    for reminder in due_reminders:
        # Send notification (in a real app, this would send an email or push notification)
        send_reminder_notification(reminder)
        
        # Update reminder status
        reminder.status = 'sent'
        reminder.save()
        count += 1
    
    return f"Processed {count} reminders"


@shared_task
def send_reminder_notification(reminder):
    """
    Send a reminder notification to the user.
    In a real application, this would send an email or push notification.
    """
    subject = f"Reminder: {reminder.title}"
    message = f"""
    Hi {reminder.user.first_name or reminder.user.username},
    
    This is a reminder for:
    
    Title: {reminder.title}
    Lead: {reminder.lead.name} - {reminder.lead.company}
    Description: {reminder.description}
    
    Please take appropriate action.
    
    Best regards,
    CRM System
    """
    
    try:
        # In production, configure email settings in settings.py
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@crm.local',
            [reminder.user.email],
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Error sending reminder notification: {e}")
        return False


@shared_task
def schedule_reminder(reminder_id):
    """
    Task to schedule a reminder notification.
    This can be called when a reminder is created to schedule it.
    """
    try:
        reminder = Reminder.objects.get(id=reminder_id)
        
        # Calculate delay until reminder time
        now = timezone.now()
        if reminder.reminder_date > now:
            delay = (reminder.reminder_date - now).total_seconds()
            # Schedule the notification
            send_reminder_notification.apply_async((reminder,), countdown=delay)
            return f"Scheduled reminder {reminder_id} for {reminder.reminder_date}"
        else:
            # Reminder is already due, send immediately
            send_reminder_notification(reminder)
            reminder.status = 'sent'
            reminder.save()
            return f"Sent overdue reminder {reminder_id}"
    except Reminder.DoesNotExist:
        return f"Reminder {reminder_id} not found"



