from django.shortcuts import render, get_object_or_404
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    print("Количество курсов:", courses.count())  # Для отладки
    return render(request, 'courses/list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/detail.html', {'course': course})
