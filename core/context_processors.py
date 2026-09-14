from .models import Document


def footer_documents(request):
    """Документы для футера"""
    return {
        'footer_documents': Document.objects.filter(is_active=True)
    }