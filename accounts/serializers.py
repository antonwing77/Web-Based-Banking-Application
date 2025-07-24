from rest_framework import serializers
from .models import Account


"""
    translates Account to and from JSON
"""
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

        fields = [
            "id",
            "owner",
            "balance",
            "status",
            "creationDate",
            "updateDate",
        ]

        read_only_fields = [
            "id",
            "creationDate",
            "updateDate",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user

        if not (user.role == 'teller' or user.role == 'admin'):
            self.fields['owner'].read_only = True

        if not user.role == 'admin':
            self.fields['balance'].read_only = True