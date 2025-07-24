from rest_framework.permissions import BasePermission

"""
    allows access only to users whose role is teller
"""
class IsTeller(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        return getattr(user, 'role', None) == 'teller'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        return getattr(user, 'role', None) == 'admin'
    
class IsTellerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        return getattr(request.user, 'role', None) in ('teller', 'admin')