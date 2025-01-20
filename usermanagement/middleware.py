import jwt
from usermanagement.utils import JWT_SECRET, JWT_ALGORITHM
from usermanagement.models import User


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                user_id = decoded.get('user_id')
                try:
                    user = User.objects.get(id=user_id)
                    request.user = user
                except User.DoesNotExist:
                    request.user = None
            except jwt.InvalidTokenError:
                request.user = None
        else:
            request.user = None

        response = self.get_response(request)

        return response