from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание')
    video = models.FileField(upload_to='courses/videos/', blank=True, null=True, verbose_name='Видео-файл')
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='courses/', verbose_name='Обложка')
    duration = models.CharField(max_length=50, verbose_name='Длительность')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']