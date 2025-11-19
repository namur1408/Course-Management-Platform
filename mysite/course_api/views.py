import jwt
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from courses_app.models import Course, Comment
from teachers_app.models import Teacher
from .serializers import CourseSerializer, CommentsSerializer, UserSerializer, TeachersSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model, authenticate
from .auth import generate_jwt_token

User = get_user_model()

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # def get_queryset(self):
    #     return Course.objects.filter(user=self.request.user)

class TeachersViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeachersSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return Course.objects.filter(user=self.request.user)

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return Course.objects.filter(user=self.request.user)

class CourseTokenObtainPairView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user:
            tokens = generate_jwt_token(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid datф for authorisation'}, status=status.HTTP_401_UNAUTHORIZED)

class CourseRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            tokens = generate_jwt_token(user)
            return Response(tokens, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            raise Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            raise Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            raise Response({'error': 'Invalid user'}, status=status.HTTP_401_UNAUTHORIZED)


