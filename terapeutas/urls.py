from django.urls import path

from . import views


urlpatterns = [
    path('terapeuta/list/', views.TerapeutaListView.as_view(), name='terapeuta-list'),
    path('terapeuta/create/', views.TerapeutaCreateView.as_view(), name='terapeuta-create'),
    path('terapeuta/<int:pk>/detail/', views.TerapeutaDetailView.as_view(), name='terapeuta-detail'),
    path('terapeuta/<int:pk>/update/', views.TerapeutaUpdateView.as_view(), name='terapeuta-update'),
    path('terapeuta/<int:pk>/delete/', views.TerapeutaDeleteView.as_view(), name='terapeuta-delete'),
    path('buscar-terapeutas/', views.buscar_terapeutas, name='buscar_terapeutas'),
]