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


class Document(models.Model):
    """Юридический документ (оферта, политика и т.д.)"""

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-код',
        help_text='Например: privacy, offer, consent. Используется в адресе страницы.'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое', help_text='Можно использовать HTML-теги')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения')
    is_active = models.BooleanField(default=True, verbose_name='Показать в футере')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['order', 'title']
