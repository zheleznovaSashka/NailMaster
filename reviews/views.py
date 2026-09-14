from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review, ScreenshotReview
from .forms import ReviewForm
from core.utils import send_notification
from core.bad_words import check_review


def review_list(request):
    """Все отзывы + скрины"""
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    screenshots = ScreenshotReview.objects.all()

    context = {
        'reviews': reviews,
        'screenshots': screenshots,
    }
    return render(request, 'reviews/list.html', context)


@login_required
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user

            has_bad_words, found_words = check_review(review.text)

            if has_bad_words:
                review.is_approved = False
                messages.warning(
                    request,
                    '⚠️ Ваш отзыв содержит запрещённые слова и отправлен на модерацию.'
                )
            else:
                review.is_approved = True
                messages.success(request, '✅ Спасибо за отзыв! Он опубликован.')

            review.save()

            status = '🚨 ТРЕБУЕТ МОДЕРАЦИИ' if has_bad_words else '✅ Опубликован'
            send_notification(
                subject=f'⭐ Новый отзыв от {request.user.username}',
                message=f'Появился новый отзыв!\n\n'
                        f'👤 Автор: {request.user.username}\n'
                        f'📝 Тип: {review.get_review_type_display()}\n'
                        f'⭐ Оценка: {review.rating}/5\n'
                        f'📊 Статус: {status}\n'
                        f'💬 Текст: {review.text}\n\n'
                        f'Проверить: http://127.0.0.1:8000/admin/reviews/review/'
            )

            return redirect('reviews:list')
    else:
        form = ReviewForm()
    return render(request, 'reviews/create.html', {'form': form})