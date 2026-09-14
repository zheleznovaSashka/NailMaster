from django.shortcuts import render, get_object_or_404
from .models import Course
from orders.models import Order


def course_list(request):
    """Список курсов"""
    courses = Course.objects.all()
    return render(request, 'courses/list.html', {'courses': courses})


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

    context = {
        'course': course,
        'has_access': has_access,
    }
    return render(request, 'courses/detail.html', context)

