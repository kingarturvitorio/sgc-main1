from django.shortcuts import render
from .import metrics

def dashboard(request):

    product_metrics = metrics.get_product_metrics

    context = {
        'product_metrics': product_metrics
    }
    return render(request, 'dashboard.html', context)
