from django.urls import path

from . import views


urlpatterns = [
    path('convenio/list/', views.ConvenioListView.as_view(), name='convenio-list'),
    path('convenio/create/', views.ConvenioCreateView.as_view(), name='convenio-create'),
    path('convenio/<int:pk>/detail/', views.ConvenioDetailView.as_view(), name='convenio-detail'),
    path('convenio/<int:pk>/update/', views.ConvenioUpdateView.as_view(), name='convenio-update'),
    path('convenio/<int:pk>/delete/', views.ConvenioDeleteView.as_view(), name='convenio-delete'),

]