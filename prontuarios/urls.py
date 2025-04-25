from django.urls import path

from . import views


urlpatterns = [
    path('prontuario/list/', views.ProntuarioListView.as_view(), name='prontuario-list'),
    path('prontuario/create/', views.ProntuarioCreateView.as_view(), name='prontuario-create'),
    path('prontuario/<int:pk>/detail/', views.ProntuarioDetailView.as_view(), name='prontuario-detail'),
    path('prontuario/<int:pk>/update/', views.ProntuarioUpdateView.as_view(), name='prontuario-update'),
    path('prontuario/<int:pk>/delete/', views.ProntuarioDeleteView.as_view(), name='prontuario-delete'),
    path('ajax/tem_prontuario/', views.verificar_prontuarios_paciente, name='verificar_prontuarios_paciente'),
]