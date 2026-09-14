from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Favorite
from portfolio.models import Work
from courses.models import Course
from core.utils import send_notification


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)

            send_notification(
                subject=f'🎉 Новый пользователь: {user.username}',
                message=f'Зарегистрировался новый пользователь!\n\n'
                        f'👤 Имя: {user.first_name} {user.last_name}\n'
                        f'📧 Email: {user.email}\n'
                        f'📞 Телефон: {user.phone or "Не указан"}\n'
                        f'📅 Дата: {user.date_joined.strftime("%d.%m.%Y %H:%M")}\n'
            )

            messages.success(request, f'🎉 Добро пожаловать, {user.first_name or user.username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, '👋 Вы вышли из аккаунта')
    return redirect('home')


@login_required
def profile_view(request):
    """Профиль с вкладками"""
    from orders.models import Order
    from reviews.models import Review

    orders_count = Order.objects.filter(user=request.user).count()
    reviews_count = Review.objects.filter(user=request.user).count()
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]

    profile_form = CustomUserChangeForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, '✅ Профиль обновлён!')
                return redirect('users:profile')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, '🔒 Пароль успешно изменён!')
                return redirect('users:profile')

    context = {
        'user': request.user,
        'profile_form': profile_form,
        'password_form': password_form,
        'orders_count': orders_count,
        'reviews_count': reviews_count,
        'recent_orders': recent_orders,
    }
    return render(request, 'users/profile.html', context)


# ==================== ИЗБРАННОЕ ====================

@login_required
def favorites_view(request):
    """Страница избранного с вкладками"""
    favorite_works = Favorite.objects.filter(
        user=request.user,
        work__isnull=False
    ).select_related('work')

    favorite_courses = Favorite.objects.filter(
        user=request.user,
        course__isnull=False
    ).select_related('course')

    context = {
        'favorite_works': [f.work for f in favorite_works],
        'favorite_courses': [f.course for f in favorite_courses],
        'works_count': favorite_works.count(),
        'courses_count': favorite_courses.count(),
    }
    return render(request, 'users/favorites.html', context)


@login_required
@require_POST
def toggle_work_favorite(request, work_id):
    """Добавить/удалить работу из избранного"""
    work = get_object_or_404(Work, pk=work_id)

    favorite = Favorite.objects.filter(user=request.user, work=work).first()

    if favorite:
        favorite.delete()
        is_favorite = False
        message = 'Удалено из избранного'
    else:
        Favorite.objects.create(user=request.user, work=work)
        is_favorite = True
        message = 'Добавлено в избранное'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite, 'message': message})

    messages.success(request, f'❤️ {message}')
    return redirect(request.META.get('HTTP_REFERER', 'portfolio:list'))


@login_required
@require_POST
def toggle_course_favorite(request, course_id):
    """Добавить/удалить курс из избранного"""
    course = get_object_or_404(Course, pk=course_id)

    favorite = Favorite.objects.filter(user=request.user, course=course).first()

    if favorite:
        favorite.delete()
        is_favorite = False
        message = 'Удалено из избранного'
    else:
        Favorite.objects.create(user=request.user, course=course)
        is_favorite = True
        message = 'Добавлено в избранное'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite, 'message': message})

    messages.success(request, f'❤️ {message}')
    return redirect(request.META.get('HTTP_REFERER', 'courses:list'))


@login_required
def clear_favorites(request):
    """Очистить всё избранное"""
    count = Favorite.objects.filter(user=request.user).count()
    Favorite.objects.filter(user=request.user).delete()
    messages.success(request, f'🗑️ Избранное очищено ({count} записей)')
    return redirect('users:favorites')