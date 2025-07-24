from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    table_name = models.CharField(max_length=50)
    record_id = models.CharField(max_length=50)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    change_timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField()  # stores changes

    def __str__(self):
        return f"{self.action} on {self.table_name} ({self.record_id}) by {self.changed_by}"