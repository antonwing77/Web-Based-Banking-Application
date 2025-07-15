from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser
import re

MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 15

def validate_password(password):
    # At least 8 chars, one uppercase, one number
    return bool(re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password))

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        address = request.data.get('address')
        city = request.data.get('city')
        state = request.data.get('state')
        zip_code = request.data.get('zip_code')

        if not validate_password(password):
            return Response({'detail': 'Password must be at least 8 characters, include one uppercase letter and one number.'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        # Save extra fields as needed
        # user.phone = phone
        # user.address = address
        # user.city = city
        # user.state = state
        # user.zip_code = zip_code
        user.save()
        return Response({'detail': 'Registration successful.'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_locked():
            return Response({'detail': f'Account locked. Try again after {user.lockout_until}.'}, status=status.HTTP_403_FORBIDDEN)

        if not validate_password(password):
            return Response({'detail': 'Password must be at least 8 characters, include one uppercase letter and one number.'}, status=status.HTTP_400_BAD_REQUEST)

        user_auth = authenticate(username=username, password=password)
        if user_auth is not None:
            user.reset_attempts()
            # ...token/session logic here
            return Response({'role': getattr(user, "role", "Client"), 'detail': 'Login successful.'})
        else:
            user.failed_attempts += 1
            if user.failed_attempts >= MAX_ATTEMPTS:
                user.lockout_until = timezone.now() + timedelta(minutes=LOCKOUT_MINUTES)
                user.save()
                return Response({'detail': f'Too many attempts. Account locked for {LOCKOUT_MINUTES} minutes.'}, status=status.HTTP_403_FORBIDDEN)
            user.save()
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)