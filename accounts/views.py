from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Account
from .serializers import AccountSerializer
from authentication.permissions import IsTeller, IsAdmin, IsTellerOrAdmin

"""
    GET - lists this user's accounts
    POST - user open's new account
"""
class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsTellerOrAdmin()]
        
        return [IsAuthenticated()]

    #show account owned by requester
    def get_queryset(self):
        user = self.request.user

        if user.role in ('admin','teller'):
            return Account.objects.all()

        return Account.objects.filter(owner=user)
    
    # create account
    def perform_create(self, serializer):
        user = self.request.user
        
        if user.role in ('teller', 'admin') and 'owner' in self.request.data:
            owner_id = self.request.data['owner']
            from django.contrib.auth import get_user_model
            User = get_user_model()

            try:
                owner = User.objects.get(pk=owner_id)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid owner ID.")
            
            serializer.save(owner=owner)

        else:
            serializer.save(owner=user)

    #  update account
    def perform_update(self, serializer):
        account = self.get_object()
        user = self.request.user

        if user.role not in ('admin','teller') and account.owner != user:
            raise exceptions.PermissionDenied("You do not have permission to update this account.")
        
        serializer.save()

    #  delete accounts, only admin and tellers can do this
    def destroy(self, request, *args, **kwargs):
        user = request.user

        if user.role not in ('teller', 'admin'):
            raise PermissionDenied("Only admin and tellers can delete accounts")

        return super().destroy(request, *args, **kwargs)

    #  returns accounts for current user
    @action(detail=False, methods=['GET'], url_path='me')
    def me(self, request):
        accounts = self.get_queryset().filter(owner=request.user)
        serializer = self.get_serializer(accounts, many=True)

        return Response(serializer.data)