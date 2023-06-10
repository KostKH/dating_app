from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomObtainAuthToken, MatchView, UserCreateView,
                    UserListViewSet)

User = get_user_model()

router = DefaultRouter()
router.register('list', UserListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('clients/create/', UserCreateView.as_view()),
    path('api-token-auth/', CustomObtainAuthToken.as_view()),
    path(r'clients/<int:id>/match/', MatchView.as_view()),
]
