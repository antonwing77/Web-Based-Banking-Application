from rest_framework import serializers
from django.conf import settings
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "client_id",
            "user_id", # foreign key from User model
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "zipcode",
            "date_of_birth",
            "email",
            "phone_number",
            "tax_id",
        ]

        read_only_fields = [
            "client_id",
            "user_id",
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            user = self.context['request'].user

            # client cannot change client_id, user_id, tax_id, or date_of_birth
            if user.role == settings.User.ROLE_CLIENT:
                for field in ('client_id','user_id','tax_id','date_of_birth'):
                    self.fields[field].read_only = True

            # teller cannot change client_id, user_id, or tax_id
            elif user.role == settings.User.ROLE_TELLER:
                for field in ('client_id','user_id','tax_id'):
                    self.fields[field].read_only = True

            # admin cannot change client_id or user_id
            elif user.role == settings.User.ROLE_ADMIN:
                for field in ('client_id','user_id'):
                    self.fields[field].read_only = True