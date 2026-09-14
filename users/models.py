from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    is_banned = models.BooleanField(default=False, verbose_name='Забанен')

    # Согласие на обработку персональных данных
    agreed_to_terms = models.BooleanField(default=False, verbose_name='Согласие с офертой')
    agreed_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата согласия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
