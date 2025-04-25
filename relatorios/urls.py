from django.urls import path

from . import views



urlpatterns = [
    path('relatorio/list/', views.RelatorioView.as_view(), name='relatorio-list'),
    path('rel_aso/<int:paciente_id>', views.rel_aso, name='rel-aso')
]