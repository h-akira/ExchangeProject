from django.urls import path
from . import views

app_name = "diary"

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('detail/<str:date>/', views.detail, name='detail'),
  path('detail/<str:date>/<str:option>/', views.detail, name='detail'),
  path('update/<str:date>/', views.update, name='update'),
  path('create/<str:date>/', views.create, name='create'),
  path('delete/<str:date>/', views.delete, name='delete'),
]

