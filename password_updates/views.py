from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser
import re
import psycopg2

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
        taxID = request.data.get('taxID')
        dob = request.data.get('dob')
        email = request.data.get('email')
        phone = request.data.get('phone')
        address = request.data.get('address')
        city = request.data.get('city')
        state = request.data.get('state')
        zip_code = request.data.get('zip_code')

        if not validate_password(password):
            return Response({'detail': 'Password must be at least 8 characters, include one uppercase letter and one number.'}, status=status.HTTP_400_BAD_REQUEST)

        # Trying to connect to SQL database
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='!12345',
                host='localhost',
                port='5432'
            )
            cur = conn.cursor()
        
            # Checking if username is already in database
            cur.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cur.fetchone():
                return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Checking if username is already in CustomUser object
            if CustomUser.objects.filter(username=username).exists():
                return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Hashing password
            hashed_pass = make_password(password)

            # Insert data into users table
            # Returns auto-incrementing user_id to use in client table
            cur.execute("INSERT INTO users (username, password, user_role) VALUES (%s, %s, %s) RETURNING user_id",
                        (username, hashed_pass, 'client')) 

            user_id = cur.fetchone()[0]

            # Insert data into client table
            cur.execute('''
                INSERT INTO client (
                    user_id, first_name, last_name, address, city, state, zipcode, date_of_birth, email, phone_number, tax_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                    (user_id, first_name, last_name, address, city, state, zip_code, dob, email, phone, taxID))

            conn.commit()
            cur.close()
            conn.close()

            return Response({'detail': 'Registration successful.'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print("Error: ", e)
            return Response({'detail': 'Server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

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
