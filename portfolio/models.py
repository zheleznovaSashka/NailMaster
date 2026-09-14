from django.db import models


class Work(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название работы')
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(upload_to='portfolio/', verbose_name='Фото работы')
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, verbose_name='На главной')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        ordering = ['-created_at']