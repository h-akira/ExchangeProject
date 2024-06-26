from django.urls import path
from . import views

app_name = "chart"

urlpatterns = [
  path('', views.index, name='index'),
  path('<int:category_number>/', views.index, name='category'),
  path('category/update/<int:pk>', views.CategoryUpdateView.as_view(), name='category_update'),
  path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
  path('category/delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category_delete'),
  path('create/', views.ChartCreateView.as_view(), name='chart_create'),
  path('delete/<int:pk>', views.ChartDeleteView.as_view(), name='chart_delete'),
  path('settings/<int:category_id>', views.chart_settings, name='chart_settings'),
  # path('detail/<str:date>/', views.detail, name='detail'),
  # path('detail/<str:date>/<str:option>/', views.detail, name='detail'),
  # path('update/<str:date>/', views.update, name='update'),
  # path('create/<str:date>/', views.create, name='create'),
  # path('delete/<str:date>/', views.delete, name='delete'),
]

