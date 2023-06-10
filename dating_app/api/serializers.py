import base64

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.core.files.base import ContentFile
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.settings import api_settings

from match.models import Match

from .utils import watermark

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):

        if isinstance(data, str) and data.startswith('data:image'):
            _, imgstr = data.split(';base64,')
            marked_image = watermark(base64.b64decode(imgstr)).getvalue()
            data = ContentFile(marked_image, name='temp.' + 'png')
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'gender',
            'avatar',
        )
        read_only_fields = ('email',)


class UserCreateMixin:
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail('cannot_create_user')
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            return User.objects.create_user(**validated_data)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)
    avatar = Base64ImageField()

    default_error_messages = {
        'cannot_create_user': 'Не удалось создать пользователя'}

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail('cannot_create_user')

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'gender',
            'avatar',
            'password',
        )

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {'password': serializer_error[
                    api_settings.NON_FIELD_ERRORS_KEY]})
        return data


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_('Email'),
        write_only=True
    )
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_('Token'),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ('liker', 'liking')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Match.objects.all(),
                fields=('liker', 'liking')
            )
        ]
