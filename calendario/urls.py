from django.urls import path

from . import views

app_name = "calendario"


urlpatterns = [
    path('calender/', views.ConsultaCreateView.as_view(), name="calendar"),
    path("calenders/", views.CalendarView.as_view(), name="calendars"),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path("event/new/", views.create_event, name="event_new"),
    path("get/event/", views.get_events, name="get_event"),
    path('confirm_event/<int:event_id>/', views.confirm_event, name='confirm_event'),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path('event/delete_all/<int:paciente_id>/', views.delete_all_events, name='delete_all_events'),
    path('filter_events/', views.filter_events, name='filter_events'),  # Add this line
    path('get_terapeutas/', views.get_terapeutas, name='get_terapeutas'),
    path('event/delete_future/<int:paciente_id>/', views.delete_future_events, name='delete-future-events'),
]
