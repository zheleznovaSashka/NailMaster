from .models import ContactInfo


def contact_info(request):
    """Передаёт контакты во все шаблоны"""
    return {
        'global_contact': ContactInfo.objects.first()
    }