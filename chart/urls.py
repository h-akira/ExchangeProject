from django.urls import path
from . import views

app_name = "chart"

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:category_number>/', views.index, name='category'),
  # path('detail/<str:date>/', views.detail, name='detail'),
  # path('detail/<str:date>/<str:option>/', views.detail, name='detail'),
  # path('update/<str:date>/', views.update, name='update'),
  # path('create/<str:date>/', views.create, name='create'),
  # path('delete/<str:date>/', views.delete, name='delete'),
]

