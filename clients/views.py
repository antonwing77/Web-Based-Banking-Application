from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, exceptions, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Client
from .serializers import ClientSerializer
from authentication.permissions import IsAdmin, IsTellerOrAdmin, IsClient, IsTeller

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    # what this user can see
    def get_queryset(self):
        user = self.request.user
        
        #admin and tellers see all
        if user.role in ('admin', 'teller'):
            return Client.objects.all()
        
        #clients only see theirs
        return Client.objects.filter(user=user)
    
    # who can do what
    def get_permissions(self):
        # only admin can creat clients
        if self.action in 'create':
            return [IsAuthenticated(), IsTellerOrAdmin()]
        
        # anyone can view
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        
        # anyone can edit/update,  what they can depends on role
        if self.action in ('update', 'partial_upddate'):
            return [IsAuthenticated()]
        
        # only admins can delete
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        
        return [IsAuthenticated()]
    
    # creating
    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'client':
            serializer.save(user=user)

        else:
            owner_id = self.request.data.get('user_id')

            if not owner_id:
                raise serializers.ValidationError({"user_id": "This field is required."})
            
            User = get_user_model()
            try:
                owner = User.objects.get(pk=owner_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"user_id": "Invalid user id."})
            serializer.save(user=owner)

        serializer.save()

    # updating
    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance

        # clients may only update their own record
        if user.role == 'client' and instance.user != user:
            raise exceptions.PermissionDenied("You can only update your own profile.")

        # disallow changing truly read‐only fields at update time
        for field in ('client_id', 'tax_id', 'date_of_birth'):
            if field in self.request.data:
                raise serializers.ValidationError({field: "You cannot update this field."})

        serializer.save()