from django.shortcuts import render, get_object_or_404
from .models import Course
from orders.models import Order
from users.models import Favorite


def course_list(request):
    """Список курсов"""
    courses = Course.objects.all()

    favorite_course_ids = []
    cart_course_ids = []
    pending_orders = {}      # {course_id: order_id}
    purchased_course_ids = []

    if request.user.is_authenticated:
        favorite_course_ids = list(
            Favorite.objects.filter(
                user=request.user,
                course__isnull=False
            ).values_list('course_id', flat=True)
        )

        cart = request.session.get('cart', {})
        cart_course_ids = [int(cid) for cid in cart.keys()]

        # Заказы в ожидании оплаты
        for order in Order.objects.filter(user=request.user, status='pending'):
            for course in order.courses.all():
                pending_orders[course.id] = order.id

        # Купленные курсы
        purchased_course_ids = list(
            Order.objects.filter(
                user=request.user,
                status__in=['paid', 'completed']
            ).values_list('courses__id', flat=True)
        )

    # ⚠️ Оборачиваем курсы в список кортежей (course, order_id)
    courses_data = []
    for course in courses:
        courses_data.append({
            'course': course,
            'pending_order_id': pending_orders.get(course.id),
        })

    context = {
        'courses_data': courses_data,
        'favorite_course_ids': favorite_course_ids,
        'cart_course_ids': cart_course_ids,
        'pending_orders': pending_orders,
        'purchased_course_ids': purchased_course_ids,
    }
    return render(request, 'courses/list.html', context)


def course_detail(request, pk):
    """Детальная страница курса"""
    course = get_object_or_404(Course, pk=pk)

    has_access = False
    pending_order = None
    in_cart = False
    is_favorite = False

    if request.user.is_authenticated:
        has_access = Order.objects.filter(
            user=request.user,
            courses=course,
            status__in=['paid', 'completed']
        ).exists()

        pending_order = Order.objects.filter(
            user=request.user,
            courses=course,
            status='pending'
        ).first()

        cart = request.session.get('cart', {})
        in_cart = str(course.id) in cart

        is_favorite = Favorite.objects.filter(
            user=request.user,
            course=course
        ).exists()

    context = {
        'course': course,
        'has_access': has_access,
        'pending_order': pending_order,
        'in_cart': in_cart,
        'is_favorite': is_favorite,
    }
    return render(request, 'courses/detail.html', context)