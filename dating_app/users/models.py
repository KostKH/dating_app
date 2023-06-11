from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CharField, CheckConstraint, EmailField,
                              FloatField, ImageField, Q, TextChoices)
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    """Класс для обработки операций с моделью User. Данный класс
    переопределяет методы создания пользователя и суперпользователя:
    были убраны ссылки на username, так как из модели мы это поле
    убрали."""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Класс User создает БД SQL для хранения
    информации о пользователях."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'gender', 'avatar']
    objects = CustomUserManager()

    class Gender(TextChoices):
        MALE = 'М', 'Мужской'
        FEMALE = 'Ж', 'Женский'
    username = None
    email = EmailField(_('email address'), blank=False, unique=True)
    first_name = CharField(_('first name'), max_length=30, blank=False)
    last_name = CharField(_('last name'), max_length=150, blank=False)
    avatar = ImageField(
        upload_to='media/',
        verbose_name='Аватар',
        help_text='Загрузите вашу фотографию',
        blank=False)

    gender = CharField(
        max_length=1,
        choices=Gender.choices,
        blank=False,
        null=False,
        verbose_name='Пол',
        help_text='Укажите ваш пол')

    latitude = FloatField(
        blank=False,
        null=False,
        default=54.9827385,
        verbose_name='Широта',
        help_text='Укажите широту вашего местоположения',
        validators=[
            MinValueValidator(
                -90.0,
                message='Должно быть значение от -90.000000 до 90.000000'),
            MaxValueValidator(
                90.0,
                message='Должно быть значение от -90.000000 до 90.000000')
        ])

    longitude = FloatField(
        blank=False,
        null=False,
        default=82.8977945,
        verbose_name='Долгота',
        help_text='Укажите долготу вашего местоположения',
        validators=[
            MinValueValidator(
                -180.0,
                message='Должно быть значение от -180.00000 до 180.000000'),
            MaxValueValidator(
                180.0,
                message='Должно быть значение от -180.000000 до 180.000000')
        ])

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            CheckConstraint(
                check=Q(latitude__gte=-90.0) & Q(latitude__lte=90.0),
                name='laptitude_between_minus90_90'),
            CheckConstraint(
                check=Q(longitude__gte=-180.0) & Q(longitude__lte=180.0),
                name='longitude_between_minus180_180'),
        ]

    def __str__(self):
        return self.email
