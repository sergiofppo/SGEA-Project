from .models import AuditLog
from users.models import Usuario

def log_action(user, action_type, details=''):
    if user and user.is_authenticated:
        AuditLog.objects.create(
            user=user,
            action=action_type,
            details=details
        )