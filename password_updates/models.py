from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import re

def validate_password(password):
    # At least 8 chars, one uppercase, one number
    return bool(re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password))

class CustomUser(AbstractUser):
    failed_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)

    def is_locked(self):
        return self.lockout_until and timezone.now() < self.lockout_until

    def reset_attempts(self):
        self.failed_attempts = 0
        self.lockout_until = None
        self.save()