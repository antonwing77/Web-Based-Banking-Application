from rest_framework import serializers
from .models import DebitCard

class DebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCard
        fields = [
            'card_number',
            'client',
            'status',
            'expiration_date',
        ]
        read_only_fields = [
            'card_number',
            'expiration_date'
        ]
