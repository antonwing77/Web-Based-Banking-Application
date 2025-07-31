from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from audit.models import AuditLog
from audit.middleware import get_current_user
from accounts.models import Account
from transactions.models import Transaction

def diff_dict(old, new):
    return {k: {'old': old[k], 'new': new[k]} for k in old if old[k] != new.get(k)}

def serialize_instance(instance):
    return {field.name: getattr(instance, field.name, None) for field in instance._meta.fields}

@receiver(post_save, sender=Account)
def audit_account_save(sender, instance, created, **kwargs):
    user = get_current_user()
    table = 'Account'
    record_id = str(instance.pk)
    changes = serialize_instance(instance)
    action = 'create' if created else 'update'

    AuditLog.objects.create(
        table_name=table,
        record_id=record_id,
        changed_by=user,
        action=action,
        changes=changes
    )

@receiver(pre_delete, sender=Account)
def audit_account_delete(sender, instance, **kwargs):
    user = get_current_user()
    table = 'Account'
    record_id = str(instance.pk)
    changes = serialize_instance(instance)
    AuditLog.objects.create(
        table_name=table,
        record_id=record_id,
        changed_by=user,
        action='delete',
        changes=changes
    )

@receiver(post_save, sender=Transaction)
def audit_transaction_save(sender, instance, created, **kwargs):
    user = get_current_user()
    table = 'Transaction'
    record_id = str(instance.pk)
    changes = serialize_instance(instance)
    action = 'create' if created else 'update'

    AuditLog.objects.create(
        table_name=table,
        record_id=record_id,
        changed_by=user,
        action=action,
        changes=changes
    )

@receiver(pre_delete, sender=Transaction)
def audit_transaction_delete(sender, instance, **kwargs):
    user = get_current_user()
    table = 'Transaction'
    record_id = str(instance.pk)
    changes = serialize_instance(instance)
    AuditLog.objects.create(
        table_name=table,
        record_id=record_id,
        changed_by=user,
        action='delete',
        changes=changes
    )