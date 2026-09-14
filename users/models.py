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

    # ✅ СОГЛАСИЯ
    consent_pd = models.BooleanField(default=False, verbose_name='Согласие на обработку ПД')
    consent_mailing = models.BooleanField(default=False, verbose_name='Согласие на рассылку')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Favorite(models.Model):
    """Избранное пользователя (работы и курсы)"""

    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    work = models.ForeignKey(
        'portfolio.Work',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='favorited_by',
        verbose_name='Работа'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='favorited_by',
        verbose_name='Курс'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'work'],
                name='unique_user_work_favorite',
                condition=models.Q(work__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_user_course_favorite',
                condition=models.Q(course__isnull=False)
            ),
        ]

    def __str__(self):
        item = self.work or self.course
        return f'{self.user.username} → {item}'
