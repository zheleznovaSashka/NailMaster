from django.shortcuts import render
from portfolio.models import Work
from courses.models import Course
from reviews.models import Review, ScreenshotReview
from core.models import MasterInfo
from contacts.models import ContactInfo
from django.shortcuts import render, get_object_or_404
from .models import Document
from django.db.models import Q


def home_view(request):
    context = {
        'master': MasterInfo.objects.first(),
        'works': Work.objects.filter(is_featured=True)[:6],
        'works_count': Work.objects.count(),           # ← ВСЕГО работ
        'courses': Course.objects.all()[:3],
        'courses_count': Course.objects.count(),       # ← ВСЕГО курсов
        'reviews': Review.objects.filter(is_approved=True)[:6],
        'screenshots': ScreenshotReview.objects.filter(is_featured=True)[:8],
        'contact': ContactInfo.objects.first(),
    }
    return render(request, 'core/home.html', context)

def document_view(request, slug):
    """Страница документа"""
    document = get_object_or_404(Document, slug=slug, is_active=True)
    return render(request, 'core/document.html', {'document': document})

def search_view(request):
    """Поиск по сайту"""
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'all')

    courses = []
    works = []

    if query:
        if search_type in ['all', 'courses']:
            courses = Course.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).order_by('-created_at')

        if search_type in ['all', 'works']:
            works = Work.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).order_by('-created_at')

    context = {
        'query': query,
        'search_type': search_type,
        'courses': courses,
        'works': works,
        'courses_count': courses.count() if query else 0,
        'works_count': works.count() if query else 0,
    }
    return render(request, 'core/search.html', context)