from django.db import models


class MasterInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя мастера')
    photo = models.ImageField(upload_to='master/', verbose_name='Фото мастера')
    about = models.TextField(verbose_name='О мастере')
    experience = models.IntegerField(verbose_name='Опыт работы (лет)', default=0)
    specialization = models.CharField(max_length=200, verbose_name='Специализация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Информация о мастере'
        verbose_name_plural = 'Информация о мастере'