from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from core.utils import send_notification


@login_required
def order_list(request):
    """Список заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    """Детали заказа"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})


@login_required
def order_cancel(request, pk):
    """Отмена заказа"""
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.status != 'pending':
        messages.error(request, '❌ Нельзя отменить заказ с этим статусом')
        return redirect('orders:detail', pk=order.pk)

    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()

        # Уведомление мастеру
        send_notification(
            subject=f'❌ Заказ #{order.id} отменен',
            message=f'Клиент отменил заказ!\n\n'
                    f'📦 Заказ: #{order.id}\n'
                    f'👤 Клиент: {request.user.username}\n'
                    f'📧 Email: {request.user.email}\n'
                    f'💰 Сумма: {order.total_price} ₽\n\n'
                    f'Проверить: http://127.0.0.1:8000/admin/orders/order/'
        )

        messages.success(request, f'✅ Заказ #{order.id} отменён')
        return redirect('orders:list')

    return render(request, 'orders/cancel.html', {'order': order})
