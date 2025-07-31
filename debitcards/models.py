from django.db import models
from django.conf import settings
from clients.models import Client

class DebitCard(models.Model):
    card_number = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, db_column='client_id', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('active','Active'),('lost','Lost'),('inactive','Inactive')])
    expiration_date = models.DateField(db_column='expiration_date')

    class Meta:
        db_table = 'debit_card'