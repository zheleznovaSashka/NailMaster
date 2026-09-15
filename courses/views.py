from django.shortcuts import render, get_object_or_404
from .models import Course
from orders.models import Order
from users.models import Favorite


def course_list(request):
    """Список курсов"""
    courses = Course.objects.all()

    favorite_course_ids = []
    cart_course_ids = []
    purchased_course_ids = []

    if request.user.is_authenticated:
        # Курсы в избранном
        favorite_course_ids = list(
            Favorite.objects.filter(
                user=request.user,
                course__isnull=False
            ).values_list('course_id', flat=True)
        )

        # Курсы в корзине
        cart = request.session.get('cart', {})
        cart_course_ids = [int(cid) for cid in cart.keys()]

        # Курсы с активными заказами (pending, paid, completed)
        purchased_course_ids = list(
            Order.objects.filter(
                user=request.user,
                status__in=['pending', 'paid', 'completed']   # ← ДОБАВИЛИ 'pending'
            ).values_list('courses__id', flat=True)
        )

    context = {
        'courses': courses,
        'favorite_course_ids': favorite_course_ids,
        'cart_course_ids': cart_course_ids,
        'purchased_course_ids': purchased_course_ids,
    }
    return render(request, 'courses/list.html', context)


def course_detail(request, pk):
    """Детальная страница курса"""
    course = get_object_or_404(Course, pk=pk)

    has_access = False
    in_cart = False
    is_favorite = False

    if request.user.is_authenticated:
        # Курс оплачен или завершён — доступ к видео
        has_access = Order.objects.filter(
            user=request.user,
            courses=course,
            status__in=['paid', 'completed']   # ← доступ только для paid/completed
        ).exists()

        # Есть активный заказ (pending, paid, completed)
        has_active_order = Order.objects.filter(
            user=request.user,
            courses=course,
            status__in=['pending', 'paid', 'completed']
        ).exists()

        # В корзине ли
        cart = request.session.get('cart', {})
        in_cart = str(course.id) in cart

        # В избранном ли
        is_favorite = Favorite.objects.filter(
            user=request.user,
            course=course
        ).exists()
    else:
        has_active_order = False

    context = {
        'course': course,
        'has_access': has_access,       # доступ к видео (только paid/completed)
        'has_active_order': has_active_order,  # есть активный заказ (включая pending)
        'in_cart': in_cart,
        'is_favorite': is_favorite,
    }
    return render(request, 'courses/detail.html', context)