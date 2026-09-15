from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from courses.models import Course
from orders.models import Order
from core.utils import send_notification


def cart_view(request):
    """Просмотр корзины"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for course_id, quantity in cart.items():
        course = get_object_or_404(Course, pk=course_id)
        subtotal = course.price * quantity
        total_price += subtotal
        cart_items.append({
            'course': course,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/view.html', context)


def add_to_cart(request, course_id):
    """Добавление курса в корзину"""
    course = get_object_or_404(Course, pk=course_id)

    if not request.user.is_authenticated:
        messages.warning(request, '🔐 Войдите, чтобы добавить курс в корзину')
        return redirect('login')

    # Проверяем, есть ли активный заказ с этим курсом
    # (pending, paid, completed — но НЕ cancelled)
    already_ordered = Order.objects.filter(
        user=request.user,
        courses=course,
        status__in=['pending', 'paid', 'completed']
    ).exists()

    if already_ordered:
        messages.info(request, f'✅ Курс "{course.title}" уже заказан! Проверьте раздел «Заказы».')
        return redirect('courses:detail', pk=course.id)

    cart = request.session.get('cart', {})

    if str(course_id) in cart:
        messages.info(request, f'🛒 Курс "{course.title}" уже в корзине!')
        return redirect('cart:view')

    cart[str(course_id)] = 1
    request.session['cart'] = cart

    messages.success(request, f'✅ Курс "{course.title}" добавлен в корзину!')
    return redirect('cart:view')


def remove_from_cart(request, course_id):
    """Удаление курса из корзины"""
    cart = request.session.get('cart', {})

    if str(course_id) in cart:
        del cart[str(course_id)]
        request.session['cart'] = cart
        messages.success(request, 'Курс удален из корзины')

    return redirect('cart:view')


def clear_cart(request):
    """Очистка корзины"""
    request.session['cart'] = {}
    messages.success(request, 'Корзина очищена')
    return redirect('cart:view')


def clear_session_cart(request):
    """Очистка корзины в сессии"""
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('home')


def checkout(request):
    """Оформление заказа"""
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, 'Корзина пуста!')
        return redirect('cart:view')

    if not request.user.is_authenticated:
        messages.warning(request, 'Для оформления заказа необходимо войти!')
        return redirect('login')

    # Создаем заказ
    cart_items = []
    total_price = 0

    for course_id, quantity in cart.items():
        course = get_object_or_404(Course, pk=course_id)
        total_price += course.price * quantity
        cart_items.append(course)

    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        status='pending'
    )
    order.courses.set(cart_items)
    order.save()

    # Уведомление мастеру
    courses_list = '\n'.join([f'  • {c.title} - {c.price} ₽' for c in cart_items])
    send_notification(
        subject=f'💰 Новый заказ #{order.id}',
        message=f'🎉 Поступил новый заказ!\n\n'
                f'📦 Заказ: #{order.id}\n'
                f'👤 Клиент: {request.user.username}\n'
                f'📧 Email: {request.user.email}\n'
                f'💰 Сумма: {total_price} ₽\n\n'
                f'📚 Курсы:\n{courses_list}\n\n'
                f'⚠️ Клиент свяжется с вами для оплаты.\n'
                f'После получения оплаты зайдите в панель управления и нажмите "💳 Оплачен".\n\n'
                f'👉 Открыть заказ: http://127.0.0.1:8000/dashboard/orders/{order.id}/'
    )

    # Очищаем корзину
    request.session['cart'] = {}

    messages.success(request, f'✅ Заказ #{order.id} оформлен! Свяжитесь со мной для оплаты.')
    return redirect('orders:detail', pk=order.id)