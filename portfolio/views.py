from django.shortcuts import render
from .models import Work
from users.models import Favorite


def portfolio_list(request):
    """Список работ"""
    works = Work.objects.all()

    # IDs работ в избранном у текущего пользователя
    favorite_work_ids = []
    if request.user.is_authenticated:
        favorite_work_ids = list(
            Favorite.objects.filter(
                user=request.user,
                work__isnull=False
            ).values_list('work_id', flat=True)
        )

    context = {
        'works': works,
        'favorite_work_ids': favorite_work_ids,
    }
    return render(request, 'portfolio/list.html', context)
