from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Q, Avg, Count
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404

from users.models import CustomUser
from orders.models import Order
from reviews.models import Review, ScreenshotReview
from portfolio.models import Work
from courses.models import Course
from core.models import MasterInfo
from contacts.models import ContactInfo
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate, TruncMonth
from core.models import Document


def is_staff(user):
    """Проверка: пользователь — админ или мастер"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(is_staff, login_url='/')
def dashboard_home(request):
    """Главная страница панели управления"""

    # Статистика
    total_users = CustomUser.objects.count()
    total_orders = Order.objects.count()
    total_reviews = Review.objects.count()
    pending_reviews = Review.objects.filter(is_approved=False).count()

    # Доход (только оплаченные и завершённые заказы)
    total_income = Order.objects.filter(
        status__in=['paid', 'completed']
    ).aggregate(total=Sum('total_price'))['total'] or 0

    # За последние 30 дней
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_orders = Order.objects.filter(created_at__gte=thirty_days_ago)
    recent_income = recent_orders.filter(
        status__in=['paid', 'completed']
    ).aggregate(total=Sum('total_price'))['total'] or 0

    # Новые пользователи за 7 дней
    seven_days_ago = timezone.now() - timedelta(days=7)
    new_users = CustomUser.objects.filter(date_joined__gte=seven_days_ago).count()

    # Контент
    works_count = Work.objects.count()
    courses_count = Course.objects.count()
    screenshots_count = ScreenshotReview.objects.count()

    # Последние заказы
    last_orders = Order.objects.order_by('-created_at')[:5]

    # Новые отзывы
    last_reviews = Review.objects.filter(is_approved=False).order_by('-created_at')[:5]

    context = {
        # Пользователи
        'total_users': total_users,
        'new_users': new_users,

        # Заказы
        'total_orders': total_orders,
        'total_income': total_income,
        'recent_income': recent_income,

        # Отзывы
        'total_reviews': total_reviews,
        'pending_reviews': pending_reviews,

        # Контент
        'works_count': works_count,
        'courses_count': courses_count,
        'screenshots_count': screenshots_count,

        # Последние
        'last_orders': last_orders,
        'last_reviews': last_reviews,
    }
    return render(request, 'dashboard/home.html', context)


# ================== УПРАВЛЕНИЕ РАБОТАМИ ==================

@login_required
@user_passes_test(is_staff, login_url='/')
def works_list(request):
    """Список всех работ"""
    works = Work.objects.all().order_by('-created_at')
    return render(request, 'dashboard/works_list.html', {'works': works})


@login_required
@user_passes_test(is_staff, login_url='/')
def work_create(request):
    """Создание новой работы"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        is_featured = request.POST.get('is_featured') == 'on'
        image = request.FILES.get('image')

        if not title or not image:
            messages.error(request, '❌ Заполните название и загрузите фото!')
        else:
            work = Work.objects.create(
                title=title,
                description=description,
                image=image,
                is_featured=is_featured,
            )
            messages.success(request, f'✅ Работа "{work.title}" добавлена!')
            return redirect('dashboard:works_list')

    return render(request, 'dashboard/work_form.html', {'action': 'create'})


@login_required
@user_passes_test(is_staff, login_url='/')
def work_edit(request, pk):
    """Редактирование работы"""
    work = get_object_or_404(Work, pk=pk)

    if request.method == 'POST':
        work.title = request.POST.get('title', work.title)
        work.description = request.POST.get('description', work.description)
        work.is_featured = request.POST.get('is_featured') == 'on'

        if request.FILES.get('image'):
            work.image = request.FILES.get('image')

        work.save()
        messages.success(request, f'✅ Работа "{work.title}" обновлена!')
        return redirect('dashboard:works_list')

    return render(request, 'dashboard/work_form.html', {'work': work, 'action': 'edit'})


@login_required
@user_passes_test(is_staff, login_url='/')
def work_delete(request, pk):
    """Удаление работы"""
    work = get_object_or_404(Work, pk=pk)

    if request.method == 'POST':
        title = work.title
        work.delete()
        messages.success(request, f'🗑️ Работа "{title}" удалена!')
        return redirect('dashboard:works_list')

    return render(request, 'dashboard/work_delete.html', {'work': work})


@login_required
@user_passes_test(is_staff, login_url='/')
def work_toggle_featured(request, pk):
    """Быстрое переключение 'На главной'"""
    work = get_object_or_404(Work, pk=pk)
    work.is_featured = not work.is_featured
    work.save()

    status = 'добавлена на главную' if work.is_featured else 'убрана с главной'
    messages.success(request, f'✅ Работа "{work.title}" {status}!')
    return redirect('dashboard:works_list')


# ================== УПРАВЛЕНИЕ КУРСАМИ ==================

@login_required
@user_passes_test(is_staff, login_url='/')
def courses_list(request):
    """Список всех курсов"""
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'dashboard/courses_list.html', {'courses': courses})


@login_required
@user_passes_test(is_staff, login_url='/')
def course_create(request):
    """Создание нового курса"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        duration = request.POST.get('duration', '')
        video = request.FILES.get('video')
        video_url = request.POST.get('video_url', '')
        image = request.FILES.get('image')

        if not title or not price or not image:
            messages.error(request, '❌ Заполните название, цену и загрузите обложку!')
        else:
            course = Course.objects.create(
                title=title,
                description=description,
                price=price,
                duration=duration,
                video=video,
                video_url=video_url,
                image=image,
            )
            messages.success(request, f'✅ Курс "{course.title}" добавлен!')
            return redirect('dashboard:courses_list')

    return render(request, 'dashboard/course_form.html', {'action': 'create'})


@login_required
@user_passes_test(is_staff, login_url='/')
def course_edit(request, pk):
    """Редактирование курса"""
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        course.title = request.POST.get('title', course.title)
        course.description = request.POST.get('description', course.description)
        course.price = request.POST.get('price', course.price)
        course.duration = request.POST.get('duration', course.duration)
        course.video_url = request.POST.get('video_url', '')

        if request.FILES.get('video'):
            course.video = request.FILES.get('video')

        if request.FILES.get('image'):
            course.image = request.FILES.get('image')

        course.save()
        messages.success(request, f'✅ Курс "{course.title}" обновлён!')
        return redirect('dashboard:courses_list')

    return render(request, 'dashboard/course_form.html', {'course': course, 'action': 'edit'})


@login_required
@user_passes_test(is_staff, login_url='/')
def course_delete(request, pk):
    """Удаление курса"""
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        title = course.title
        course.delete()
        messages.success(request, f'🗑️ Курс "{title}" удалён!')
        return redirect('dashboard:courses_list')

    return render(request, 'dashboard/course_delete.html', {'course': course})


# ================== УПРАВЛЕНИЕ СКРИНАМИ ОТЗЫВОВ ==================

@login_required
@user_passes_test(is_staff, login_url='/')
def screenshots_list(request):
    """Список всех скринов"""
    screenshots = ScreenshotReview.objects.all().order_by('order', '-created_at')
    return render(request, 'dashboard/screenshots_list.html', {'screenshots': screenshots})


@login_required
@user_passes_test(is_staff, login_url='/')
def screenshot_create(request):
    """Создание нового скрина"""
    if request.method == 'POST':
        title = request.POST.get('title', '')
        source = request.POST.get('source', 'other')
        order = request.POST.get('order', 0)
        is_featured = request.POST.get('is_featured') == 'on'
        image = request.FILES.get('image')

        if not image:
            messages.error(request, '❌ Загрузите скрин отзыва!')
        else:
            screenshot = ScreenshotReview.objects.create(
                title=title,
                source=source,
                order=order,
                is_featured=is_featured,
                image=image,
            )
            messages.success(request, f'✅ Скрин добавлен!')
            return redirect('dashboard:screenshots_list')

    return render(request, 'dashboard/screenshot_form.html', {'action': 'create'})


@login_required
@user_passes_test(is_staff, login_url='/')
def screenshot_edit(request, pk):
    """Редактирование скрина"""
    screenshot = get_object_or_404(ScreenshotReview, pk=pk)

    if request.method == 'POST':
        screenshot.title = request.POST.get('title', '')
        screenshot.source = request.POST.get('source', screenshot.source)
        screenshot.order = request.POST.get('order', screenshot.order)
        screenshot.is_featured = request.POST.get('is_featured') == 'on'

        if request.FILES.get('image'):
            screenshot.image = request.FILES.get('image')

        screenshot.save()
        messages.success(request, '✅ Скрин обновлён!')
        return redirect('dashboard:screenshots_list')

    return render(request, 'dashboard/screenshot_form.html', {'screenshot': screenshot, 'action': 'edit'})


@login_required
@user_passes_test(is_staff, login_url='/')
def screenshot_delete(request, pk):
    """Удаление скрина"""
    screenshot = get_object_or_404(ScreenshotReview, pk=pk)

    if request.method == 'POST':
        screenshot.delete()
        messages.success(request, '🗑️ Скрин удалён!')
        return redirect('dashboard:screenshots_list')

    return render(request, 'dashboard/screenshot_delete.html', {'screenshot': screenshot})


@login_required
@user_passes_test(is_staff, login_url='/')
def screenshot_toggle_featured(request, pk):
    """Быстрое переключение 'На главной'"""
    screenshot = get_object_or_404(ScreenshotReview, pk=pk)
    screenshot.is_featured = not screenshot.is_featured
    screenshot.save()

    status = 'добавлен на главную' if screenshot.is_featured else 'убран с главной'
    messages.success(request, f'✅ Скрин {status}!')
    return redirect('dashboard:screenshots_list')


# ================== УПРАВЛЕНИЕ ОТЗЫВАМИ ==================

@login_required
@user_passes_test(is_staff, login_url='/')
def reviews_list(request):
    """Список всех отзывов с фильтром"""
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'pending':
        reviews = Review.objects.filter(is_approved=False).order_by('-created_at')
    elif filter_type == 'approved':
        reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    else:
        reviews = Review.objects.all().order_by('-created_at')

    # Счётчики
    total_count = Review.objects.count()
    pending_count = Review.objects.filter(is_approved=False).count()
    approved_count = Review.objects.filter(is_approved=True).count()

    context = {
        'reviews': reviews,
        'filter_type': filter_type,
        'total_count': total_count,
        'pending_count': pending_count,
        'approved_count': approved_count,
    }
    return render(request, 'dashboard/reviews_list.html', context)


@login_required
@user_passes_test(is_staff, login_url='/')
def review_approve(request, pk):
    """Одобрить отзыв"""
    review = get_object_or_404(Review, pk=pk)
    review.is_approved = True
    review.save()
    messages.success(request, f'✅ Отзыв от {review.user.username} одобрен!')
    return redirect('dashboard:reviews_list')


@login_required
@user_passes_test(is_staff, login_url='/')
def review_reject(request, pk):
    """Отклонить отзыв (скрыть)"""
    review = get_object_or_404(Review, pk=pk)
    review.is_approved = False
    review.save()
    messages.warning(request, f'⚠️ Отзыв от {review.user.username} отклонён!')
    return redirect('dashboard:reviews_list')


@login_required
@user_passes_test(is_staff, login_url='/')
def review_delete(request, pk):
    """Удалить отзыв"""
    review = get_object_or_404(Review, pk=pk)

    if request.method == 'POST':
        username = review.user.username
        review.delete()
        messages.success(request, f'🗑️ Отзыв от {username} удалён!')
        return redirect('dashboard:reviews_list')

    return render(request, 'dashboard/review_delete.html', {'review': review})


# ================== ИНФОРМАЦИЯ О МАСТЕРЕ ==================

@login_required
@user_passes_test(is_staff, login_url='/')
def master_edit(request):
    """Редактирование информации о мастере"""
    master = MasterInfo.objects.first()

    if not master:
        master = MasterInfo.objects.create(
            name='Мастер',
            about='Информация о мастере',
            experience=0,
            specialization='',
        )

    if request.method == 'POST':
        master.name = request.POST.get('name', master.name)
        master.about = request.POST.get('about', master.about)
        master.experience = request.POST.get('experience', master.experience)
        master.specialization = request.POST.get('specialization', master.specialization)

        if request.FILES.get('photo'):
            master.photo = request.FILES.get('photo')

        master.save()
        messages.success(request, '✅ Информация о мастере обновлена!')
        return redirect('dashboard:master_edit')

    return render(request, 'dashboard/master_edit.html', {'master': master})


# ================== КОНТАКТЫ ==================

@login_required
@user_passes_test(is_staff, login_url='/')
def contacts_edit(request):
    """Редактирование контактной информации"""
    contact = ContactInfo.objects.first()

    if not contact:
        contact = ContactInfo.objects.create(
            phone='',
            email='',
        )

    if request.method == 'POST':
        contact.phone = request.POST.get('phone', contact.phone)
        contact.email = request.POST.get('email', contact.email)
        contact.telegram = request.POST.get('telegram', '')
        contact.max_messenger = request.POST.get('max_messenger', '')
        contact.booking_url = request.POST.get('booking_url', '')
        contact.save()

        messages.success(request, '✅ Контакты обновлены!')
        return redirect('dashboard:contacts_edit')

    return render(request, 'dashboard/contacts_edit.html', {'contact': contact})


# ================== УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ ==================

@login_required
@user_passes_test(is_staff, login_url='/')
def users_list(request):
    """Список всех пользователей с поиском"""
    search_query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', 'all')

    users = CustomUser.objects.all().order_by('-date_joined')

    # Фильтр по статусу
    if filter_type == 'staff':
        users = users.filter(Q(is_staff=True) | Q(is_superuser=True))
    elif filter_type == 'banned':
        users = users.filter(is_banned=True)
    elif filter_type == 'active':
        users = users.filter(is_banned=False)

    # Поиск
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    # Счётчики
    total_count = CustomUser.objects.count()
    banned_count = CustomUser.objects.filter(is_banned=True).count()
    staff_count = CustomUser.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).count()

    context = {
        'users': users,
        'search_query': search_query,
        'filter_type': filter_type,
        'total_count': total_count,
        'banned_count': banned_count,
        'staff_count': staff_count,
    }
    return render(request, 'dashboard/users_list.html', context)


@login_required
@user_passes_test(is_staff, login_url='/')
def user_detail(request, pk):
    """Детальная информация о пользователе"""
    user_obj = get_object_or_404(CustomUser, pk=pk)

    # Статистика пользователя
    orders = Order.objects.filter(user=user_obj).order_by('-created_at')
    reviews = Review.objects.filter(user=user_obj).order_by('-created_at')

    context = {
        'user_obj': user_obj,
        'orders': orders,
        'reviews': reviews,
        'orders_count': orders.count(),
        'reviews_count': reviews.count(),
        'total_spent': orders.filter(status__in=['paid', 'completed']).aggregate(
            total=Sum('total_price')
        )['total'] or 0,
    }
    return render(request, 'dashboard/user_detail.html', context)


@login_required
@user_passes_test(is_staff, login_url='/')
def user_toggle_ban(request, pk):
    """Забанить/разбанить пользователя"""
    user_obj = get_object_or_404(CustomUser, pk=pk)

    # Нельзя банить себя
    if user_obj == request.user:
        messages.error(request, '❌ Нельзя забанить себя!')
        return redirect('dashboard:users_list')

    # Нельзя банить админов
    if user_obj.is_superuser:
        messages.error(request, '❌ Нельзя забанить администратора!')
        return redirect('dashboard:users_list')

    user_obj.is_banned = not user_obj.is_banned
    user_obj.save()

    status = 'забанен' if user_obj.is_banned else 'разбанен'
    messages.success(request, f'✅ Пользователь {user_obj.username} {status}!')

    # Возврат на ту же страницу
    next_page = request.GET.get('next', 'dashboard:users_list')
    if next_page == 'detail':
        return redirect('dashboard:user_detail', pk=pk)
    return redirect('dashboard:users_list')


@login_required
@user_passes_test(is_staff, login_url='/')
def user_toggle_staff(request, pk):
    """Сделать пользователя админом/убрать права"""
    user_obj = get_object_or_404(CustomUser, pk=pk)

    # Нельзя менять себя
    if user_obj == request.user:
        messages.error(request, '❌ Нельзя менять свои права!')
        return redirect('dashboard:users_list')

    # Только суперюзер может назначать админов
    if not request.user.is_superuser:
        messages.error(request, '❌ Только главный администратор может менять права!')
        return redirect('dashboard:users_list')

    user_obj.is_staff = not user_obj.is_staff
    user_obj.save()

    status = 'назначен администратором' if user_obj.is_staff else 'лишён прав администратора'
    messages.success(request, f'✅ Пользователь {user_obj.username} {status}!')
    return redirect('dashboard:users_list')


# ================== УПРАВЛЕНИЕ ЗАКАЗАМИ ==================

@login_required
@user_passes_test(is_staff, login_url='/')
def orders_list(request):
    """Список всех заказов"""
    filter_type = request.GET.get('filter', 'all')

    orders = Order.objects.all().order_by('-created_at')

    if filter_type == 'pending':
        orders = orders.filter(status='pending')
    elif filter_type == 'paid':
        orders = orders.filter(status='paid')
    elif filter_type == 'completed':
        orders = orders.filter(status='completed')
    elif filter_type == 'cancelled':
        orders = orders.filter(status='cancelled')

    # Счётчики
    total_count = Order.objects.count()
    pending_count = Order.objects.filter(status='pending').count()
    paid_count = Order.objects.filter(status='paid').count()
    completed_count = Order.objects.filter(status='completed').count()
    cancelled_count = Order.objects.filter(status='cancelled').count()

    context = {
        'orders': orders,
        'filter_type': filter_type,
        'total_count': total_count,
        'pending_count': pending_count,
        'paid_count': paid_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
    }
    return render(request, 'dashboard/orders_list.html', context)


@login_required
@user_passes_test(is_staff, login_url='/')
def order_detail_dashboard(request, pk):
    """Детали заказа (для мастера)"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return render(request, 'dashboard/order_not_found.html', {'order_id': pk}, status=404)

    return render(request, 'dashboard/order_detail.html', {'order': order})


@login_required
@user_passes_test(is_staff, login_url='/')
def order_change_status(request, pk, status):
    """Изменение статуса заказа"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        messages.error(request, f'❌ Заказ #{pk} не найден')
        return redirect('dashboard:orders_list')

    valid_statuses = ['pending', 'paid', 'completed', 'cancelled']
    if status not in valid_statuses:
        messages.error(request, '❌ Неверный статус')
        return redirect('dashboard:orders_list')

    order.status = status
    order.save()


    status_names = {
        'pending': '⏳ Ожидает оплаты',
        'paid': '💳 Оплачен',
        'completed': '✅ Завершён',
        'cancelled': '❌ Отменён',
    }

    messages.success(request, f'✅ Заказ #{order.id}: {status_names[status]}')

    next_page = request.GET.get('next', 'list')
    if next_page == 'detail':
        return redirect('dashboard:order_detail', pk=pk)
    return redirect('dashboard:orders_list')


@login_required
@user_passes_test(is_staff, login_url='/')
def order_delete(request, pk):
    """Удаление заказа"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        messages.error(request, f'❌ Заказ #{pk} не найден или уже удалён')
        return redirect('dashboard:orders_list')

    if request.method == 'POST':
        order_id = order.id
        order.delete()
        messages.success(request, f'🗑️ Заказ #{order_id} удалён!')
        return redirect('dashboard:orders_list')

    return render(request, 'dashboard/order_delete.html', {'order': order})


@login_required
@user_passes_test(is_staff, login_url='/')
def stats_view(request):
    """Расширенная статистика"""

    # === ДОХОД ЗА 30 ДНЕЙ ===
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)

    # Группировка по дням
    daily_income = Order.objects.filter(
        created_at__date__gte=thirty_days_ago,
        status__in=['paid', 'completed']
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        total=Sum('total_price'),
        count=Count('id')
    ).order_by('date')

    # Заполняем пропущенные дни
    days_data = {}
    for i in range(31):
        d = thirty_days_ago + timedelta(days=i)
        days_data[d] = {'total': 0, 'count': 0}

    for item in daily_income:
        days_data[item['date']] = {
            'total': float(item['total'] or 0),
            'count': item['count']
        }

    # Данные для графика
    chart_labels = [d.strftime('%d.%m') for d in days_data.keys()]
    chart_income = [data['total'] for data in days_data.values()]
    chart_orders = [data['count'] for data in days_data.values()]

    # === СТАТУСЫ ЗАКАЗОВ ===
    status_stats = Order.objects.values('status').annotate(
        count=Count('id')
    )

    status_data = {
        'pending': 0,
        'paid': 0,
        'completed': 0,
        'cancelled': 0,
    }
    for s in status_stats:
        status_data[s['status']] = s['count']

    # === ТОП КУРСОВ ===
    top_courses = Course.objects.annotate(
        orders_count=Count('order')
    ).filter(orders_count__gt=0).order_by('-orders_count')[:5]

    # === ТОП КЛИЕНТОВ ===
    top_clients = CustomUser.objects.annotate(
        orders_count=Count('order'),
        total_spent=Sum('order__total_price',
                        filter=Q(order__status__in=['paid', 'completed']))
    ).filter(orders_count__gt=0).order_by('-total_spent')[:5]

    # === РЕЙТИНГ ОТЗЫВОВ ===
    rating_stats = Review.objects.values('rating').annotate(
        count=Count('id')
    ).order_by('rating')

    rating_data = {i: 0 for i in range(1, 6)}
    for r in rating_stats:
        rating_data[r['rating']] = r['count']

    # === СРЕДНИЙ ЧЕК ===
    avg_order = Order.objects.filter(
        status__in=['paid', 'completed']
    ).aggregate(avg=Avg('total_price'))['avg'] or 0

    # === ОБЩАЯ СТАТИСТИКА ===
    total_stats = {
        'total_users': CustomUser.objects.count(),
        'new_users_month': CustomUser.objects.filter(
            date_joined__gte=timezone.now() - timedelta(days=30)
        ).count(),
        'total_orders': Order.objects.count(),
        'orders_month': Order.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
        'total_income': Order.objects.filter(
            status__in=['paid', 'completed']
        ).aggregate(total=Sum('total_price'))['total'] or 0,
        'avg_order': avg_order,
    }

    # === СТАТИСТИКА ПО МЕСЯЦАМ (последние 6 месяцев) ===
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_income = Order.objects.filter(
        created_at__gte=six_months_ago,
        status__in=['paid', 'completed']
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Sum('total_price'),
        count=Count('id')
    ).order_by('month')

    month_labels = []
    month_income = []
    month_orders = []

    for item in monthly_income:
        month_labels.append(item['month'].strftime('%m.%Y'))
        month_income.append(float(item['total'] or 0))
        month_orders.append(item['count'])

    context = {
        'total_stats': total_stats,
        'chart_labels': chart_labels,
        'chart_income': chart_income,
        'chart_orders': chart_orders,
        'status_data': status_data,
        'top_courses': top_courses,
        'top_clients': top_clients,
        'rating_data': rating_data,
        'month_labels': month_labels,
        'month_income': month_income,
        'month_orders': month_orders,
    }
    return render(request, 'dashboard/stats.html', context)


def order_not_found(request, pk=None):
    """Страница 'Заказ не найден'"""
    return render(request, 'dashboard/order_not_found.html', {'order_id': pk}, status=404)


# ================== УПРАВЛЕНИЕ ДОКУМЕНТАМИ ==================

@login_required
@user_passes_test(is_staff, login_url='/')
def documents_list(request):
    """Список документов"""
    documents = Document.objects.all().order_by('order', 'title')
    return render(request, 'dashboard/documents_list.html', {'documents': documents})


@login_required
@user_passes_test(is_staff, login_url='/')
def document_create(request):
    """Создание документа"""
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        content = request.POST.get('content', '')
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'

        if not title or not slug:
            messages.error(request, '❌ Заполните заголовок и URL-код!')
        else:
            Document.objects.create(
                title=title,
                slug=slug,
                content=content,
                order=order,
                is_active=is_active,
            )
            messages.success(request, f'✅ Документ "{title}" создан!')
            return redirect('dashboard:documents_list')

    return render(request, 'dashboard/document_form.html', {'action': 'create'})


@login_required
@user_passes_test(is_staff, login_url='/')
def document_edit(request, pk):
    """Редактирование документа"""
    document = get_object_or_404(Document, pk=pk)

    if request.method == 'POST':
        document.title = request.POST.get('title', document.title)
        document.slug = request.POST.get('slug', document.slug)
        document.content = request.POST.get('content', document.content)
        document.order = request.POST.get('order', document.order)
        document.is_active = request.POST.get('is_active') == 'on'
        document.save()

        messages.success(request, f'✅ Документ "{document.title}" обновлён!')
        return redirect('dashboard:documents_list')

    return render(request, 'dashboard/document_form.html', {'document': document, 'action': 'edit'})


@login_required
@user_passes_test(is_staff, login_url='/')
def document_delete(request, pk):
    """Удаление документа"""
    document = get_object_or_404(Document, pk=pk)

    if request.method == 'POST':
        title = document.title
        document.delete()
        messages.success(request, f'🗑️ Документ "{title}" удалён!')
        return redirect('dashboard:documents_list')

    return render(request, 'dashboard/document_delete.html', {'document': document})

