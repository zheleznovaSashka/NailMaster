from django.shortcuts import render
from .models import ContactInfo

def contact_view(request):
    contact = ContactInfo.objects.first()
    return render(request, 'contacts/index.html', {'contact': contact})