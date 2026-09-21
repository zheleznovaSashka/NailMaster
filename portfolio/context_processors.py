from .models import Work


def recent_works(request):
    """Недавно просмотренные работы"""
    recent_ids = request.session.get('recent_works', [])

    if not recent_ids:
        return {'recent_works': []}

    works_dict = {w.id: w for w in Work.objects.filter(id__in=recent_ids)}
    recent = [works_dict[wid] for wid in recent_ids if wid in works_dict]

    return {'recent_works': recent}
