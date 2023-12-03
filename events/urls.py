from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
  # path('', views.IndexView.as_view(), name='index'),
  path('detail/<int:id>/', views.detail, name='detail'),
  path('detail/<int:id>/<str:option>/', views.detail, name='detail'),
  path('update/<int:id>/', views.update, name='update'),
  path('create/<int:id>/', views.create, name='create'),
  path('delete/<int:id>/', views.delete, name='delete'),
]
