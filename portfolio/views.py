from django.shortcuts import render, get_object_or_404
from .models import Work, WorkView
from users.models import Favorite


def portfolio_list(request):
    """Список работ"""
    works = Work.objects.all()

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


def portfolio_detail(request, pk):
    """Детальная страница работы"""
    work = get_object_or_404(Work, pk=pk)

    # ✅ Проверяем: считать ли просмотр
    should_count = False

    # 1. Админ — НЕ считаем
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        should_count = False

    # 2. Авторизованный пользователь — считаем 1 раз навсегда
    elif request.user.is_authenticated:
        already_viewed = WorkView.objects.filter(
            work=work,
            user=request.user
        ).exists()

        if not already_viewed:
            WorkView.objects.create(work=work, user=request.user)
            should_count = True

    # 3. Гость — считаем 1 раз за сессию
    else:
        # Убедимся, что у сессии есть ключ
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        already_viewed = WorkView.objects.filter(
            work=work,
            session_key=session_key
        ).exists()

        if not already_viewed:
            WorkView.objects.create(work=work, session_key=session_key)
            should_count = True

    # Увеличиваем счётчик только если нужно
    if should_count:
        work.views += 1
        work.save(update_fields=['views'])

    # ✅ Добавляем в "недавно просмотренные"
    recent = request.session.get('recent_works', [])
    if pk in recent:
        recent.remove(pk)
    recent.insert(0, pk)
    recent = recent[:8]
    request.session['recent_works'] = recent
    request.session.modified = True

    # Избранное
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            work=work
        ).exists()

    context = {
        'work': work,
        'is_favorite': is_favorite,
    }
    return render(request, 'portfolio/detail.html', context)

