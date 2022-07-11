from django.shortcuts import render


def index_page(request):
    """Standard view function - prevents app from crashing on root path /"""
    return render(request, 'index.html')
