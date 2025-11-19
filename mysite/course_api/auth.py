import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class CourseJwtAuth(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid user')

def generate_jwt_token(user):
    token_payload = {
        'user_id': user.id,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=5),
        'iat': datetime.now(timezone.utc)
    }

    access_payload = token_payload.copy()
    refresh_payload = token_payload.copy()
    refresh_payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=10)

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return {
        'access': access_token,
        'refresh': refresh_token
    }


