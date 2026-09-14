from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    courses = models.ManyToManyField(Course, verbose_name='Курсы')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итого')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID платежа')

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']