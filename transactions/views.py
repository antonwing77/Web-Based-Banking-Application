from django.shortcuts import render
from rest_framework import viewsets, exceptions, status, serializers, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Transaction
from .serializers import TransactionSerializer
from authentication.permissions import IsTeller, IsAdmin, IsTellerOrAdmin
from decimal import Decimal

"""
    clients can list and create transactions on their account
    tellers and admins can flag transactions
    admins can delete transactions
"""
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdmin()]
        
        elif self.action == 'flag':
            return [IsAuthenticated(), IsTellerOrAdmin()]
        
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role in ('admin', 'teller'):
            return Transaction.objects.all()
        
        # only show users transactions
        return Transaction.objects.filter(account__owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        transaction = serializer.save()
        transaction.owner = self.request.user
        account = transaction.account
        amount = Decimal(transaction.amount)

        if user.role == 'client' and account.owner != user:
            raise exceptions.PermissionDenied("Cannot transact on an account you do not own.")
        
        if amount <= 0:
            raise serializers.ValidationError("Transaction amount must be positive.")
        

        if transaction.type == 'deposit':
            account.balance += amount

        elif transaction.type == 'withdrawal':
            if amount > account.balance:
                raise serializers.ValidationError("Insufficient funds for withdrawal.")
            
            account.balance -= amount

        else:
            raise serializers.ValidationError("Unknown transaction type.")

        account.save()
        transaction.save()

    # delete transaction, only admin can do this
    def destroy(self, request, *args, **kwargs):
        user = request.user
        
        if user.role != 'admin':
            raise PermissionDenied("Only admin can delete transactions.")
        
        return super().destroy(request, *args, **kwargs)

    # mark a transaction as flagged
    @action(detail=True,  methods=['post'],  permission_classes=[IsAuthenticated, IsTellerOrAdmin])
    def flag(self, request, pk=None):
        transaction = self.get_object()
        transaction.flagged = True
        transaction.save()

        serializer = self.get_serializer(transaction)

        return Response(serializer.data, status=status.HTTP_200_OK)
