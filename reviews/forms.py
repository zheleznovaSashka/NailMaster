from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_type', 'text', 'rating', 'image']
        widgets = {
            'review_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Расскажите о вашем опыте...',
            }),
            'rating': forms.Select(
                choices=[(i, f'{i} ⭐') for i in range(1, 6)],
                attrs={'class': 'form-control'}
            ),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
        labels = {
            'review_type': 'О чём отзыв?',
            'text': 'Ваш отзыв',
            'rating': 'Оценка',
            'image': 'Фото (необязательно)',
        }