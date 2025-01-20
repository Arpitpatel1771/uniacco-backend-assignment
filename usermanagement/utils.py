import jwt
import datetime
from django.conf import settings

JWT_SECRET = "KLAJDNMN!@#!@#NMN<MN!@#!@#"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY = 15  # in minutes
REFRESH_TOKEN_EXPIRY = 7  # in days

def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'name': user.name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRY),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def generate_refresh_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRY),
        'iat': datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token
