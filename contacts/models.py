from django.db import models


class ContactInfo(models.Model):
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    instagram = models.URLField(blank=True, null=True, verbose_name='Instagram')
    telegram = models.URLField(blank=True, null=True, verbose_name='Telegram')
    max_messenger = models.URLField(blank=True, null=True, verbose_name='MAX')
    booking_url = models.URLField(verbose_name='Ссылка на запись', blank=True)

    def __str__(self):
        return "Контактная информация"

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'