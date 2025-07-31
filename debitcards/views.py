from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import DebitCard
from .serializers import DebitCardSerializer
from authentication.permissions import IsClient, IsTeller, IsAdmin, IsTellerOrAdmin
from clients.models import Client

class DebitCardViewSet(viewsets.ModelViewSet):
    serializer_class = DebitCardSerializer
    queryset = DebitCard.objects.all()

    def get_queryset(self):
        user = self.request.user

        # clients only their own
        if user.role == user.ROLE_CLIENT:
            return DebitCard.objects.filter(client__user=user)
        
        # tellers & admins see all
        if user.role in (user.ROLE_TELLER, user.ROLE_ADMIN):
            return DebitCard.objects.all()
        
        return DebitCard.objects.none()

    def get_permissions(self):

        if self.action in ('create',):
            return [IsAuthenticated(), IsTellerOrAdmin()]

        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]

        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role not in (user.ROLE_ADMIN, user.ROLE_TELLER):
            raise PermissionDenied("Only tellers or admins can issue cards.")

        client_id = self.request.data.get("client")
        if not client_id:
            raise ValidationError({"client": "This field is required."})

        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            raise ValidationError({"client": "Invalid client id."})

        serializer.save(client=client)


    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()
        supplied = set(self.request.data.keys())

        # clients can only toggle status on their cards
        if user.role == user.ROLE_CLIENT:
            if instance.client.user != user:
                raise PermissionDenied("Cannot edit someone else's card.")
            
            if supplied - {"status"}:
                raise PermissionDenied("Clients may only update card status.")
            
        # tellers can only toggle status
        elif user.role == user.ROLE_TELLER:
            if supplied - {"status"}:
                raise PermissionDenied("Tellers may only update card status.")

        serializer.save()