from math import pi

from django.contrib.auth import get_user_model
from django.db.models import ExpressionWrapper, F, FloatField, Func
from django_filters import rest_framework as filters

User = get_user_model()


class Sin(Func):
    function = 'SIN'


class Atan(Func):
    function = 'ATAN'


class Cos(Func):
    function = 'COS'


class Abs(Func):
    function = 'ABS'


class UserListFilter(filters.FilterSet):
    """Класс, задающий фильтры для просмотра списка пользователей."""

    distance = filters.NumberFilter(method='get_distance')

    class Meta:
        model = User
        fields = ('gender', 'first_name', 'last_name', 'distance')

    def get_distance(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            latitude = self.request.user.latitude * pi / 180
            longitude = self.request.user.longitude * pi / 180
            latitude2 = F('latitude') * pi / 180
            longitude2 = F('longitude') * pi / 180
            earth_radius_km = 6372.795
            formula = Abs(Atan(
                ((Cos(latitude2) * Sin(longitude2 - longitude)) ** 2
                 + (Cos(latitude) * Sin(latitude2)
                    - Sin(latitude) * Cos(latitude2)
                    * Cos(longitude2 - longitude)) ** 2) ** (1 / 2)
                / (Sin(latitude) * Sin(latitude2)
                    + Cos(latitude) * Cos(latitude2)
                    * Cos(longitude2 - longitude))
            )) * earth_radius_km
            distance_query = ExpressionWrapper(
                formula,
                output_field=FloatField()
            )
            return queryset.annotate(
                distance=distance_query
            ).filter(distance__lte=float(value))
        return queryset
