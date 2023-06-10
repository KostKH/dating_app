from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from match.models import Match
from match.tasks import match_notification

from .serializers import (CustomAuthTokenSerializer, MatchSerializer,
                          UserCreateSerializer)

User = get_user_model()


class UserCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer


class MatchView(APIView):

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
