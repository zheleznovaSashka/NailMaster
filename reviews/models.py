from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    """Текстовый отзыв от пользователя сайта"""
    TYPE_CHOICES = [
        ('master', 'О мастере'),
        ('work', 'О работе'),
        ('course', 'О курсе'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    review_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип отзыва')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='Оценка')
    image = models.ImageField(upload_to='reviews/', blank=True, null=True, verbose_name='Фото отзыва')
    is_approved = models.BooleanField(default=True, verbose_name='Опубликован')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']


class ScreenshotReview(models.Model):
    """Скрин отзыва с другой площадки (Instagram, WhatsApp, VK)"""

    SOURCE_CHOICES = [
        ('instagram', 'Instagram'),
        ('max', 'MAX'),
        ('telegram', 'Telegram'),
        ('vk', 'VK'),
        ('avito', 'Avito'),
        ('yandex', 'Яндекс'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок', blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other', verbose_name='Источник')
    image = models.ImageField(upload_to='reviews/screenshots/', verbose_name='Скрин отзыва')
    is_featured = models.BooleanField(default=False, verbose_name='На главной')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Скрин #{self.id}"

    class Meta:
        verbose_name = 'Скрин отзыва'
        verbose_name_plural = 'Скрины отзывов'
        ordering = ['order', '-created_at']