from django.shortcuts import render
from .models import Work

def portfolio_list(request):
    works = Work.objects.all()
    return render(request, 'portfolio/list.html', {'works': works})
