from django.db import models
from django.conf import settings

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        db_column='user_id',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    tax_id = models.CharField(max_length=20)

    class Meta:
        db_table = 'client'
        ordering = ('client_id',)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (User: {self.user.username})"
