from django.shortcuts import render, get_object_or_404
from .models import Course
from orders.models import Order
from users.models import Favorite


def course_list(request):
    """Список курсов"""
    courses = Course.objects.all()

    # IDs курсов в избранном
    favorite_course_ids = []
    if request.user.is_authenticated:
        favorite_course_ids = list(
            Favorite.objects.filter(
                user=request.user,
                course__isnull=False
            ).values_list('course_id', flat=True)
        )

    context = {
        'courses': courses,
        'favorite_course_ids': favorite_course_ids,
    }
    return render(request, 'courses/list.html', context)


def course_detail(request, pk):
    """Детальная страница курса"""
    course = get_object_or_404(Course, pk=pk)

    # Проверяем, купил ли пользователь этот курс
    has_access = False
    if request.user.is_authenticated:
        has_access = Order.objects.filter(
            user=request.user,
            courses=course,
            status__in=['paid', 'completed']
        ).exists()

    # Проверяем, в избранном ли
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            course=course
        ).exists()

    context = {
        'course': course,
        'has_access': has_access,
        'is_favorite': is_favorite,
    }
    return render(request, 'courses/detail.html', context)

