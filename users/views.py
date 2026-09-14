from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from core.utils import send_notification
from django.utils import timezone


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
                        f'📅 Дата: {user.date_joined.strftime("%d.%m.%Y %H:%M")}\n\n'
                        f'Проверить: http://127.0.0.1:8000/admin/users/customuser/'
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

    # Статистика
    orders_count = Order.objects.filter(user=request.user).count()
    reviews_count = Review.objects.filter(user=request.user).count()
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Формы
    profile_form = CustomUserChangeForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    # Обработка POST
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
                update_session_auth_hash(request, user)  # Чтобы не разлогинило
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
