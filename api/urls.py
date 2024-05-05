from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
  path(
    "get_data_by_date/<str:date>/<str:pair>/<str:rule>/",
    views.get_data_by_date,
    name="get_data_by_date"
  ),
  path(
    "get_latest_data_by_yf/<str:pair>/<str:rule>/",
    views.get_latest_data_by_yf,
    name="get_latest_data_by_yf"
  ),
  path(
    "get_data_by_event/<int:event_id>/<str:pair>/<str:rule>/",
    views.get_data_by_event,
    name="get_data_by_event"
  ),
  path('events_json/', views.events_json, name='events_json'),
]
