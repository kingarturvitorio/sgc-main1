from django.urls import path

from . import views


urlpatterns = [
    path('paciente/list/', views.PacienteListView.as_view(), name='paciente-list'),
    path('paciente/create/', views.PacienteCreateView.as_view(), name='paciente-create'),
    path('paciente/<int:pk>/detail/', views.PacienteDetailView.as_view(), name='paciente-detail'),
    path('paciente/<int:pk>/update/', views.PacienteUpdateView.as_view(), name='paciente-update'),
    path('paciente/<int:pk>/delete/', views.PacienteDeleteView.as_view(), name='paciente-delete'),
    path('buscar-pacientes/', views.buscar_pacientes, name='buscar_pacientes'),

]