from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
  path(
    "get_data_by_date/<str:date>/<str:pair>/<str:rule>/",
    views.get_data_by_date,
    name="get_data_by_date"
  ),
  path('events_json/', views.events_json, name='events_json'),
]
