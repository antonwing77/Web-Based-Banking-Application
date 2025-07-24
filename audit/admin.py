from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('table_name', 'record_id', 'changed_by', 'action', 'change_timestamp')
    search_fields = ('table_name', 'record_id', 'changed_by__username')
    readonly_fields = ('table_name', 'record_id', 'changed_by', 'action', 'change_timestamp', 'changes')