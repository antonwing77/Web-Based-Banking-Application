from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, ChangePasswordSerializer
from .permissions import IsAdmin, IsClient, IsTeller, IsTellerOrAdmin

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    persmission_classes = [IsAuthenticated()]

    """
        Pick permissions based on action:
            only admins can list or destroy
            authenticated users can retrieve/update their own
            only admins/tellers can use the change-password action below
    """
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]

        if self.action in ('list', 'destroy'):
            return [IsAuthenticated(), IsAdmin()]
        
        if self.action in ('update', 'partial_update', 'retrieve'):
            return [IsAuthenticated()]
        
        if self.action == 'change_password':
            return [IsAuthenticated(), IsTellerOrAdmin()]
        
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        # only admins may list everyone
        if user.role == user.ROLE_ADMIN:
            return User.objects.all()
        
        # non-admins may only see themselves
        return User.objects.filter(pk=user.pk)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)

        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        ser = ChangePasswordSerializer(data=request.data, context={'request':request})
        ser.is_valid(raise_exception=True)
        request.user.set_password(ser.validated_data['new_password'])
        request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='change_password')
    def change_password(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(status=204)