from django.contrib.auth import get_user_model
from django.urls import path

from .views import CustomObtainAuthToken, MatchView, UserCreateView

User = get_user_model()

urlpatterns = [
    path('clients/create/', UserCreateView.as_view()),
    path('api-token-auth/', CustomObtainAuthToken.as_view()),
    path(r'clients/<int:id>/match/', MatchView.as_view()),
]
