from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

"""
    defines status for an Account
"""
class AccountStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    CLOSED = "closed", "Closed"
    FROZEN = "frozen", "Frozen"

"""
    bank account belonging to a User
"""
class Account(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts"
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE
    )

    creationDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    """
        to string
    """
    def __str__(self):
        return f"Account #{self.id} ({self.owner.username}) - ${self.balance}"