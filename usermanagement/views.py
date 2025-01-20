import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Token
from .utils import generate_access_token, generate_refresh_token, JWT_SECRET, JWT_ALGORITHM
import json

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            country = data.get('country', '')

            if not name or not email or not password:
                return JsonResponse({'error': 'Name, email, and password are required.'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists.'}, status=400)

            user = User(name=name, email=email, country=country)
            user.set_password(password)
            user.save()

            return JsonResponse({'message': 'User registered successfully.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required.'}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Invalid email or password.'}, status=401)

            if not user.check_password(password):
                return JsonResponse({'error': 'Invalid email or password.'}, status=401)

            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            Token.objects.update_or_create(user=user, defaults={'refresh_token': refresh_token})

            return JsonResponse({'access_token': access_token, 'refresh_token': refresh_token}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def refresh(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            refresh_token = data.get('refresh_token')

            if not refresh_token:
                return JsonResponse({'error': 'Refresh token is required.'}, status=400)

            try:
                decoded = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                user_id = decoded.get('user_id')

                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Invalid refresh token.'}, status=403)

                if not user.token.refresh_token == refresh_token:
                    return JsonResponse({'error': 'Invalid refresh token.'}, status=403)

                access_token = generate_access_token(user)
                return JsonResponse({'access_token': access_token}, status=200)

            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Refresh token has expired.'}, status=403)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token.'}, status=403)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)