from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'amount', 'type', 'timestamp', 'flagged']
        read_only_fields = ['id', 'flagged', 'timestamp']