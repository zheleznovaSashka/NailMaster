from django.db import models


class Work(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название работы')
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(upload_to='portfolio/', verbose_name='Фото работы')
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, verbose_name='На главной')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        ordering = ['-created_at']


class WorkView(models.Model):
    """Кто и когда смотрел работу (для защиты от накрутки)"""
    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name='work_views',
        verbose_name='Работа'
    )
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    session_key = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name='Ключ сессии'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        verbose_name = 'Просмотр работы'
        verbose_name_plural = 'Просмотры работ'
        # Защита: 1 пользователь — 1 просмотр на работу
        constraints = [
            models.UniqueConstraint(
                fields=['work', 'user'],
                name='unique_user_work_view',
                condition=models.Q(user__isnull=False)
            ),
        ]

    def __str__(self):
        who = self.user.username if self.user else f'Гость ({self.session_key[:8]})'
        return f'{who} → {self.work.title}'