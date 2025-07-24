from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # the three roles
    ROLE_CLIENT = 'client'
    ROLE_TELLER = 'teller'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_CLIENT, 'Client'),
        (ROLE_TELLER, 'Teller'),
        (ROLE_ADMIN, 'Admin'),
    ]

    # add the role
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_CLIENT,
    )