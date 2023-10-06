from django.urls import path
from . import views

app_name = "diary"

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('detail/<str:date>/', views.detail, name='detail'),
  path('events_json/', views.events_json, name='events_json'),
]

