from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from match.models import Match
from match.tasks import match_notification

from .filters import UserListFilter
from .serializers import (CustomAuthTokenSerializer, MatchSerializer,
                          UserCreateSerializer, UserSerializer)

User = get_user_model()


class UserCreateView(APIView):
    """Класс для обработки эндпойнта на создание пользователя."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    """Класс для обработки эндпойнта создания токена авторизации."""

    serializer_class = CustomAuthTokenSerializer


class MatchView(APIView):
    """Класс для обработки эндпойнта на создание мэтча пользователей."""

    def post(self, request, id=None):
        data = {
            'liker': request.user.id,
            'liking': id
        }
        serializer = MatchSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            resp_data = serializer.data.copy()
            try:
                reverse_match = Match.objects.get(
                    liking_id=request.user.id,
                    liker_id=id)

                resp_data['liking_email'] = reverse_match.liker.email
                match_notification.delay(
                    request.user.first_name,
                    request.user.email,
                    reverse_match.liker.first_name,
                    reverse_match.liker.email)

            except Match.DoesNotExist:
                pass
            return Response(resp_data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class UserListViewSet(ListModelMixin, GenericViewSet):
    """Класс для обработки эндпойнта на вывод списка пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserListFilter
